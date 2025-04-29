def estimate_arrival_time(distance_km: float) -> int:
    """
    Estimates the time of arrival in minutes based on the distance (km).
    Assumes an average speed of 40 km/h and a minimum of 5 minutes.
    """
    if distance_km <= 0:
        return 5
    speed_kmh = 40
    hours = distance_km / speed_kmh
    minutes = hours * 60
    return max(5, round(minutes))
