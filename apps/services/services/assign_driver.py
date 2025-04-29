from django.db import transaction

from apps.drivers.models.driver import Driver
from apps.services.choices.status_service import ServiceStatus
from apps.services.methods.calculate_distance import calculate_distance
from apps.services.methods.estimate_arrival_time import estimate_arrival_time
from apps.services.models.service import Service


@transaction.atomic
def assign_driver_to_service(service: Service):
    """
    Finds the nearest available driver and assigns it to the given service.
    Calculates the estimated arrival time based on distance.
    """
    available_drivers = Driver.objects.filter(is_available=True).select_related(
        "current_location"
    )

    if not available_drivers.exists():
        raise Exception("No available drivers at the moment.")

    nearest_driver = None
    min_distance = None

    client_lat = service.client_address.latitude
    client_lng = service.client_address.longitude

    for driver in available_drivers:
        driver_lat = driver.current_location.latitude
        driver_lng = driver.current_location.longitude
        distance = calculate_distance(driver_lat, driver_lng, client_lat, client_lng)

        if min_distance is None or distance < min_distance:
            nearest_driver = driver
            min_distance = distance

    if nearest_driver is None:
        raise Exception("Unable to find a suitable driver.")

    service.driver = nearest_driver
    service.status = ServiceStatus.IN_PROGRESS
    service.estimated_time_minutes = estimate_arrival_time(distance_km=min_distance)
    service.save()

    nearest_driver.available = False
    nearest_driver.save()

    return service
