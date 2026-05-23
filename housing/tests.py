from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from . import services
from .exceptions import HousingValidationError, HousingNotFoundError
from .models import House, MaintenanceRequest, Resident

User = get_user_model()


class ServiceLayerTests(TestCase):
    def setUp(self):
        self.house_one = House.objects.create(
            address='1 Test Street',
            city='Darwin',
            state='NT',
            zip_code='0800',
            rent=500,
        )
        self.house_two = House.objects.create(
            address='2 Test Street',
            city='Darwin',
            state='NT',
            zip_code='0801',
            rent=600,
        )
        self.resident = Resident.objects.create(
            house=self.house_one,
            first_name='Ava',
            last_name='Taylor',
            email='ava@example.com',
        )

    def test_create_house_persists_clean_data(self):
        house = services.create_house({
            'address': '9 New Road',
            'city': 'Alice Springs',
            'state': 'NT',
            'zip_code': '0870',
            'rent': 750,
        })
        self.assertEqual(House.objects.count(), 3)
        self.assertEqual(house.city, 'Alice Springs')

    def test_create_house_strips_whitespace(self):
        house = services.create_house({
            'address': '  123 Main St  ',
            'city': '  Darwin  ',
            'state': 'NT',
            'zip_code': '0800',
        })
        self.assertEqual(house.address, '123 Main St')
        self.assertEqual(house.city, 'Darwin')

    def test_update_house_modifies_existing_record(self):
        services.update_house(self.house_one, {
            'address': '99 Updated Lane',
            'city': 'Darwin',
            'state': 'NT',
            'zip_code': '0800',
        })
        self.house_one.refresh_from_db()
        self.assertEqual(self.house_one.address, '99 Updated Lane')

    def test_create_resident_requires_house(self):
        with self.assertRaises(HousingValidationError):
            services.create_resident({'first_name': 'John', 'last_name': 'Doe', 'house': None})

    def test_update_resident_changes_house(self):
        services.update_resident(self.resident, {
            'first_name': 'Ava',
            'last_name': 'Taylor',
            'house': self.house_two,
        })
        self.resident.refresh_from_db()
        self.assertEqual(self.resident.house_id, self.house_two.id)

    def test_create_request_requires_title(self):
        with self.assertRaises(HousingValidationError):
            services.create_request({
                'house': self.house_one,
                'resident': self.resident,
                'title': None,
            })

    def test_create_request_rejects_cross_house_resident(self):
        with self.assertRaises(HousingValidationError):
            services.create_request({
                'house': self.house_two,
                'resident': self.resident,
                'title': 'Leaking tap',
                'description': 'Kitchen tap leaks at night.',
                'status': MaintenanceRequest.Status.PENDING,
                'category': MaintenanceRequest.Category.PLUMBING,
            })

    def test_delete_house_is_blocked_when_dependents_exist(self):
        MaintenanceRequest.objects.create(
            house=self.house_one,
            resident=self.resident,
            title='Broken light',
            description='Hall light is not working.',
        )
        with self.assertRaises(HousingValidationError):
            services.delete_house(self.house_one)

    def test_delete_resident_blocked_when_requests_exist(self):
        MaintenanceRequest.objects.create(
            house=self.house_one,
            resident=self.resident,
            title='Leaking tap',
        )
        with self.assertRaises(HousingValidationError):
            services.delete_resident(self.resident)

    def test_list_operations_return_correct_counts(self):
        self.assertEqual(len(services.list_houses()), 2)
        self.assertEqual(len(services.list_residents()), 1)

    def test_delete_request_succeeds(self):
        req = MaintenanceRequest.objects.create(
            house=self.house_one,
            resident=self.resident,
            title='Leaking tap',
        )
        services.delete_request(req)
        self.assertEqual(MaintenanceRequest.objects.count(), 0)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Secret12345')

    def test_registration_page_is_accessible(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Your Account')

    def test_register_creates_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'password1': 'SecurePass123!',
                'password2': 'SecurePass123!',
            },
            follow=True,
        )
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_is_accessible(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_successful_with_valid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'Secret12345'},
            follow=True,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_removes_session(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_navbar_shows_login_link_when_anonymous(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')

    def test_navbar_shows_logout_link_when_authenticated(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'testuser')


class HouseCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Secret12345')
        self.house = House.objects.create(
            address='10 View Street',
            city='Darwin',
            state='NT',
            zip_code='0800',
            rent=420,
        )

    def test_house_list_is_public(self):
        response = self.client.get(reverse('house_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '10 View Street')

    def test_house_list_shows_house_details(self):
        response = self.client.get(reverse('house_list'))
        self.assertContains(response, 'Darwin')
        self.assertContains(response, 'NT')

    def test_house_create_requires_login(self):
        response = self.client.get(reverse('house_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_house_create_requires_login_post(self):
        response = self.client.post(reverse('house_create'), {'address': 'New House'})
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_house(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('house_create'),
            {
                'address': '11 New Street',
                'city': 'Alice Springs',
                'state': 'NT',
                'zip_code': '0870',
                'rent': 500,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(House.objects.filter(address='11 New Street').exists())

    def test_house_update_requires_login(self):
        response = self.client.get(reverse('house_update', args=[self.house.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_update_house(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('house_update', args=[self.house.id]),
            {
                'address': '10 Updated Street',
                'city': 'Darwin',
                'state': 'NT',
                'zip_code': '0800',
                'rent': 450,
            },
            follow=True,
        )
        self.house.refresh_from_db()
        self.assertEqual(self.house.address, '10 Updated Street')

    def test_house_delete_requires_login(self):
        response = self.client.get(reverse('house_delete', args=[self.house.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_delete_house_if_no_dependents(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('house_delete', args=[self.house.id]),
            follow=True,
        )
        self.assertFalse(House.objects.filter(id=self.house.id).exists())


class ResidentCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Secret12345')
        self.house = House.objects.create(
            address='10 View Street',
            city='Darwin',
            state='NT',
            zip_code='0800',
        )

    def test_resident_list_is_public(self):
        response = self.client.get(reverse('resident_list'))
        self.assertEqual(response.status_code, 200)

    def test_resident_create_requires_login(self):
        response = self.client.get(reverse('resident_create'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_resident(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('resident_create'),
            {
                'first_name': 'Jordan',
                'last_name': 'Lee',
                'email': 'jordan@example.com',
                'phone': '0400000000',
                'house': self.house.pk,
            },
            follow=True,
        )
        self.assertTrue(Resident.objects.filter(first_name='Jordan').exists())

    def test_resident_update_requires_login(self):
        resident = Resident.objects.create(
            house=self.house,
            first_name='Jordan',
            last_name='Lee',
        )
        response = self.client.get(reverse('resident_update', args=[resident.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_update_resident(self):
        resident = Resident.objects.create(
            house=self.house,
            first_name='Jordan',
            last_name='Lee',
        )
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('resident_update', args=[resident.id]),
            {
                'first_name': 'Jordan',
                'last_name': 'Smith',
                'house': self.house.pk,
            },
            follow=True,
        )
        resident.refresh_from_db()
        self.assertEqual(resident.last_name, 'Smith')

    def test_resident_delete_requires_login(self):
        resident = Resident.objects.create(
            house=self.house,
            first_name='Jordan',
            last_name='Lee',
        )
        response = self.client.get(reverse('resident_delete', args=[resident.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_delete_resident_if_no_requests(self):
        resident = Resident.objects.create(
            house=self.house,
            first_name='Jordan',
            last_name='Lee',
        )
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('resident_delete', args=[resident.id]),
            follow=True,
        )
        self.assertFalse(Resident.objects.filter(id=resident.id).exists())


class RequestCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Secret12345')
        self.house = House.objects.create(
            address='10 View Street',
            city='Darwin',
            state='NT',
            zip_code='0800',
        )
        self.resident = Resident.objects.create(
            house=self.house,
            first_name='Jordan',
            last_name='Lee',
        )

    def test_request_list_is_public(self):
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.status_code, 200)

    def test_request_create_requires_login(self):
        response = self.client.get(reverse('request_create'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_request(self):
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('request_create'),
            {
                'house': self.house.pk,
                'resident': self.resident.pk,
                'title': 'Leaking tap',
                'description': 'Kitchen tap leaks at night',
                'status': MaintenanceRequest.Status.PENDING,
                'category': MaintenanceRequest.Category.PLUMBING,
            },
            follow=True,
        )
        self.assertTrue(MaintenanceRequest.objects.filter(title='Leaking tap').exists())

    def test_request_update_requires_login(self):
        request_obj = MaintenanceRequest.objects.create(
            house=self.house,
            resident=self.resident,
            title='Leaking tap',
        )
        response = self.client.get(reverse('request_update', args=[request_obj.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_update_request(self):
        request_obj = MaintenanceRequest.objects.create(
            house=self.house,
            resident=self.resident,
            title='Leaking tap',
        )
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('request_update', args=[request_obj.id]),
            {
                'house': self.house.pk,
                'resident': self.resident.pk,
                'title': 'Leaking tap - URGENT',
                'description': 'Getting worse',
                'status': MaintenanceRequest.Status.IN_PROGRESS,
                'category': MaintenanceRequest.Category.PLUMBING,
            },
            follow=True,
        )
        request_obj.refresh_from_db()
        self.assertEqual(request_obj.title, 'Leaking tap - URGENT')

    def test_request_delete_requires_login(self):
        request_obj = MaintenanceRequest.objects.create(
            house=self.house,
            resident=self.resident,
            title='Leaking tap',
        )
        response = self.client.get(reverse('request_delete', args=[request_obj.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_delete_request(self):
        request_obj = MaintenanceRequest.objects.create(
            house=self.house,
            resident=self.resident,
            title='Leaking tap',
        )
        self.client.login(username='testuser', password='Secret12345')
        response = self.client.post(
            reverse('request_delete', args=[request_obj.id]),
            follow=True,
        )
        self.assertFalse(MaintenanceRequest.objects.filter(id=request_obj.id).exists())


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.house1 = House.objects.create(
            address='House 1',
            city='Darwin',
            state='NT',
            zip_code='0800',
        )
        self.house2 = House.objects.create(
            address='House 2',
            city='Alice Springs',
            state='NT',
            zip_code='0870',
        )
        self.resident = Resident.objects.create(
            house=self.house1,
            first_name='John',
            last_name='Doe',
        )

    def test_home_page_shows_summary_stats(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '2')
        self.assertContains(response, '1')

    def test_home_page_shows_recent_requests(self):
        req = MaintenanceRequest.objects.create(
            house=self.house1,
            resident=self.resident,
            title='Test Request',
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Request')
