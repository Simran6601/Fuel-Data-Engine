from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import math


def get_coordinates(location_name):

    try:

        geolocator = Nominatim(
            user_agent="fueldata_engine",
            timeout=10
        )

        location = geolocator.geocode(
            location_name
        )

        if not location:
            return None

        return (
            location.latitude,
            location.longitude
        )

    except Exception:
        return None


def calculate_distance(
    start_coords,
    end_coords
):

    return geodesic(
        start_coords,
        end_coords
    ).miles


def midpoint(
    start_coords,
    end_coords
):

    return (
        (
            start_coords[0] +
            end_coords[0]
        ) / 2,
        (
            start_coords[1] +
            end_coords[1]
        ) / 2
    )


def distance_from_point(
    point_a,
    point_b
):

    return geodesic(
        point_a,
        point_b
    ).miles


def get_osrm_route(
    start_coords,
    end_coords
):

    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        if (
            "routes" not in data
            or not data["routes"]
        ):
            return None

        return data["routes"][0]

    except Exception:
        return None


def get_route_checkpoints(
    route_geometry,
    distance,
    vehicle_range=500
):

    required_stops = max(
        0,
        math.ceil(
            distance / vehicle_range
        ) - 1
    )

    checkpoints = []

    if required_stops == 0:
        return checkpoints

    total_points = len(
        route_geometry
    )

    for i in range(
        1,
        required_stops + 1
    ):

        index = int(
            (
                i /
                (required_stops + 1)
            ) * total_points
        )

        checkpoints.append(
            route_geometry[index]
        )

    return checkpoints