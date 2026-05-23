from django.db import transaction

from .exceptions import HousingNotFoundError, HousingValidationError
from .models import House, MaintenanceRequest, Resident


def dashboard_summary():
    return {
        "houses": House.objects.count(),
        "residents": Resident.objects.count(),
        "requests": MaintenanceRequest.objects.count(),
        "open_requests": MaintenanceRequest.objects.exclude(
            status=MaintenanceRequest.Status.RESOLVED
        ).count(),
    }


def recent_requests(limit=5):
    return (
        MaintenanceRequest.objects.select_related("house", "resident")
        .order_by("-created_at")[:limit]
    )


def list_houses():
    return House.objects.prefetch_related("residents").order_by("address", "city")


def list_requests():
    return MaintenanceRequest.objects.select_related("house", "resident").order_by(
        "-created_at"
    )


def list_residents():
    return Resident.objects.select_related("house").order_by("last_name", "first_name")


@transaction.atomic
def create_house(data):
    _validate_required_fields(data, ["address", "city", "state", "zip_code"])
    return House.objects.create(
        address=data["address"].strip(),
        city=data["city"].strip(),
        state=data["state"].strip(),
        zip_code=data["zip_code"].strip(),
        rent=data.get("rent"),
        num_bedrooms=data.get("num_bedrooms"),
        num_bathrooms=data.get("num_bathrooms"),
        is_available=data.get("is_available", True),
    )


@transaction.atomic
def update_house(house, data):
    _validate_required_fields(data, ["address", "city", "state", "zip_code"])
    house.address = data["address"].strip()
    house.city = data["city"].strip()
    house.state = data["state"].strip()
    house.zip_code = data["zip_code"].strip()
    house.rent = data.get("rent")
    house.num_bedrooms = data.get("num_bedrooms")
    house.num_bathrooms = data.get("num_bathrooms")
    house.is_available = data.get("is_available", house.is_available)
    house.save()
    return house


@transaction.atomic
def delete_house(house):
    if house.residents.exists() or house.maintenance_requests.exists():
        raise HousingValidationError(
            "This house cannot be deleted while residents or requests still exist."
        )
    house.delete()


@transaction.atomic
def create_resident(data):
    _validate_required_fields(data, ["first_name", "last_name", "house"])
    house = _resolve_house(data["house"])
    return Resident.objects.create(
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        email=data.get("email") or None,
        phone=data.get("phone") or None,
        house=house,
        move_in_date=data.get("move_in_date"),
        move_out_date=data.get("move_out_date"),
    )


@transaction.atomic
def update_resident(resident, data):
    _validate_required_fields(data, ["first_name", "last_name", "house"])
    resident.first_name = data["first_name"].strip()
    resident.last_name = data["last_name"].strip()
    resident.email = data.get("email") or None
    resident.phone = data.get("phone") or None
    resident.house = _resolve_house(data["house"])
    resident.move_in_date = data.get("move_in_date")
    resident.move_out_date = data.get("move_out_date")
    resident.save()
    return resident


@transaction.atomic
def delete_resident(resident):
    if resident.maintenance_requests.exists():
        raise HousingValidationError(
            "This resident cannot be deleted while maintenance requests still exist."
        )
    resident.delete()


@transaction.atomic
def create_request(data):
    _validate_required_fields(data, ["house", "resident", "title"])
    house = _resolve_house(data["house"])
    resident = _resolve_resident(data["resident"])
    _ensure_resident_matches_house(resident, house)
    return MaintenanceRequest.objects.create(
        house=house,
        resident=resident,
        title=data["title"].strip(),
        description=data.get("description") or "",
        status=data.get("status") or MaintenanceRequest.Status.PENDING,
        category=data.get("category") or MaintenanceRequest.Category.OTHER,
    )


@transaction.atomic
def update_request(request_obj, data):
    _validate_required_fields(data, ["house", "resident", "title"])
    house = _resolve_house(data["house"])
    resident = _resolve_resident(data["resident"])
    _ensure_resident_matches_house(resident, house)
    request_obj.house = house
    request_obj.resident = resident
    request_obj.title = data["title"].strip()
    request_obj.description = data.get("description") or ""
    request_obj.status = data.get("status") or MaintenanceRequest.Status.PENDING
    request_obj.category = data.get("category") or MaintenanceRequest.Category.OTHER
    request_obj.save()
    return request_obj


@transaction.atomic
def delete_request(request_obj):
    request_obj.delete()


def _validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        joined = ", ".join(missing)
        raise HousingValidationError(f"Missing required field(s): {joined}.")


def _resolve_house(value):
    if isinstance(value, House):
        return value
    try:
        return House.objects.get(pk=value)
    except House.DoesNotExist as exc:
        raise HousingNotFoundError("The selected house could not be found.") from exc


def _resolve_resident(value):
    if isinstance(value, Resident):
        return value
    try:
        return Resident.objects.select_related("house").get(pk=value)
    except Resident.DoesNotExist as exc:
        raise HousingNotFoundError("The selected resident could not be found.") from exc


def _ensure_resident_matches_house(resident, house):
    if resident.house_id != house.id:
        raise HousingValidationError("The selected resident must belong to the selected house.")
