from django.db import models


class House(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    num_bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    num_bathrooms = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.city}"


class Resident(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="residents")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    move_in_date = models.DateField(blank=True, null=True)
    move_out_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.house})"


class MaintenanceRequest(models.Model):
    class Status:
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"
        RESOLVED = "RESOLVED"
        REJECTED = "REJECTED"

        CHOICES = (
            (PENDING, "Pending"),
            (IN_PROGRESS, "In Progress"),
            (RESOLVED, "Resolved"),
            (REJECTED, "Rejected"),
        )

    class Category:
        PLUMBING = "PLUMBING"
        ELECTRICAL = "ELECTRICAL"
        HVAC = "HVAC"
        PAINTING = "PAINTING"
        STRUCTURAL = "STRUCTURAL"
        OTHER = "OTHER"

        CHOICES = (
            (PLUMBING, "Plumbing"),
            (ELECTRICAL, "Electrical"),
            (HVAC, "HVAC"),
            (PAINTING, "Painting"),
            (STRUCTURAL, "Structural"),
            (OTHER, "Other"),
        )

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="maintenance_requests")
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="maintenance_requests")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=Status.CHOICES, default=Status.PENDING)
    category = models.CharField(max_length=32, choices=Category.CHOICES, default=Category.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} - {self.house}"