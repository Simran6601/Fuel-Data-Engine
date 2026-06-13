from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Avg, Min, Max

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FuelStation
from django.core.cache import cache

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter
)

from .utils import (
    get_coordinates,
    calculate_distance,
    midpoint,
    distance_from_point,
    get_osrm_route,
    get_route_checkpoints
)

import math
import time
import logging
# Assignment Constants

logger = logging.getLogger(__name__)

VEHICLE_RANGE = 500
VEHICLE_MPG = 10
MAX_STATION_DISTANCE = 100

@api_view(["GET"])
def health_check(request):

    return Response({
        "status": "healthy",
        "service": "FuelData Engine"
    })

def fuel_stations(request):

    state = request.GET.get("state")
    city = request.GET.get("city")

    page = int(
        request.GET.get(
            "page",
            1
        )
    )

    page_size = int(
        request.GET.get(
            "page_size",
            20
        )
    )

    stations = FuelStation.objects.all()

    if state:
        stations = stations.filter(
            state=state.upper()
        )

    if city:
        stations = stations.filter(
            city__icontains=city
        )

    total_records = stations.count()

    start_index = (
        (page - 1)
        * page_size
    )

    end_index = (
        start_index
        + page_size
    )

    stations = stations[
        start_index:end_index
    ]

    data = []

    for station in stations:

        data.append({
            "truckstop_name":
            station.truckstop_name,

            "city":
            station.city.strip(),

            "state":
            station.state,

            "retail_price":
            station.retail_price
        })

    return JsonResponse({

        "page":
        page,

        "page_size":
        page_size,

        "total_records":
        total_records,

        "results":
        data
    })


def cheapest_stations(request):

    limit = int(
        request.GET.get("limit", 10)
    )

    stations = FuelStation.objects.order_by(
        "retail_price"
    )[:limit]

    data = []

    for station in stations:

        data.append({
            "truckstop_name": station.truckstop_name,
            "city": station.city,
            "state": station.state,
            "retail_price": station.retail_price
        })

    return JsonResponse(
        data,
        safe=False
    )


def station_stats(request):

    stats = FuelStation.objects.aggregate(
        average_price=Avg("retail_price"),
        cheapest_price=Min("retail_price"),
        highest_price=Max("retail_price")
    )

    return JsonResponse({

        "total_stations":
        FuelStation.objects.count(),

        "states_covered":
        FuelStation.objects.values(
            "state"
        ).distinct().count(),

        "average_price":
        round(
            stats["average_price"] or 0,
            3
        ),

        "cheapest_price":
        stats["cheapest_price"] or 0,

        "highest_price":
        stats["highest_price"] or 0
    })




def state_prices(request):

    states = FuelStation.objects.values(
        "state"
    ).annotate(
        average_price=Avg(
            "retail_price"
        )
    ).order_by(
        "average_price"
    )

    data = []

    for state in states:

        data.append({

            "state":
            state["state"],

            "average_price":
            round(
                state["average_price"],
                3
            )
        })

    return JsonResponse(
        data,
        safe=False
    )

@csrf_exempt
def route_cost(request):

    try:

        distance = float(
            request.GET.get(
                "distance",
                1200
            )
        )

        mileage = float(
            request.GET.get(
                "mileage",
                10
            )
        )

    except ValueError:

        logger.info(
        f"Fuel cost calculated for {distance} miles"
        )

        return JsonResponse(
            {
                "error":
                "Distance and mileage must be numeric values"
            },
            status=400
        )

    if mileage <= 0:

        return JsonResponse(
            {
                "error":
                "Mileage must be greater than 0"
            },
            status=400
        )

    if distance <= 0:

        return JsonResponse(
            {
                "error":
                "Distance must be greater than 0"
            },
            status=400
        )

    avg_price = (
        FuelStation.objects.aggregate(
            Avg("retail_price")
        )["retail_price__avg"]
        or 0
    )

    fuel_needed = distance / mileage

    estimated_cost = (
        fuel_needed *
        avg_price
    )

    return JsonResponse({

        "distance":
        distance,

        "mileage":
        mileage,

        "fuel_needed":
        round(
            fuel_needed,
            2
        ),

        "average_fuel_price":
        round(
            avg_price,
            3
        ),

        "estimated_cost":
        round(
            estimated_cost,
            2
        )
    })


@csrf_exempt
def route_optimizer(request):

    try:

        distance = float(
            request.GET.get(
                "distance",
                1200
            )
        )

        mileage = float(
            request.GET.get(
                "mileage",
                10
            )
        )

        tank_capacity = float(
            request.GET.get(
                "tank_capacity",
                100
            )
        )

    except ValueError:

     logger.warning(
        "Invalid route optimization request"
    )

    return JsonResponse(
        {
            "error":
            "Distance, mileage and tank capacity must be numeric values"
        },
        status=400
    )

    if mileage <= 0:

        return JsonResponse(
            {
                "error":
                "Mileage must be greater than 0"
            },
            status=400
        )

    if distance <= 0:

        return JsonResponse(
            {
                "error":
                "Distance must be greater than 0"
            },
            status=400
        )

    if tank_capacity <= 0:

        return JsonResponse(
            {
                "error":
                "Tank capacity must be greater than 0"
            },
            status=400
        )
    fuel_needed = distance / mileage

    max_distance_per_tank = (
        tank_capacity *
        mileage
    )

    refuel_stops = int(
        fuel_needed //
        tank_capacity
    )

    avg_price = (
    FuelStation.objects.aggregate(
        Avg("retail_price")
    )["retail_price__avg"]
    or 0
    )

    estimated_cost = (
        fuel_needed *
        avg_price
    )

    stations = FuelStation.objects.filter(
        latitude__isnull=False
    ).order_by(
        "retail_price"
    )[:5]

    recommended_stations = []

    for station in stations:

        recommended_stations.append({
            "truckstop_name":
            station.truckstop_name,
            "city":
            station.city,
            "state":
            station.state,
            "retail_price":
            station.retail_price
        })

    return JsonResponse({

        "distance":
        distance,

        "mileage":
        mileage,

        "tank_capacity":
        tank_capacity,

        "fuel_needed":
        round(
            fuel_needed,
            2
        ),

        "max_distance_per_tank":
        round(
            max_distance_per_tank,
            2
        ),

        "refuel_stops":
        refuel_stops,

        "estimated_cost":
        round(
            estimated_cost,
            2
        ),

        "recommended_stations":
        recommended_stations
    })

@api_view(["GET"])
def route_planner(request):

    start_time = time.time()

    start = request.GET.get("start")
    end = request.GET.get("end")

    if not start or not end:
        return Response(
            {
                "error":
                "Please provide start and end locations"
            },
            status=400
        )

    cache_key = f"route_{start}_{end}"

    cached_response = cache.get(cache_key)

    if cached_response:
        return Response(cached_response)

    start_coords = get_coordinates(start)
    end_coords = get_coordinates(end)

    if not start_coords or not end_coords:
        return Response(
            {
                "error":
                "Unable to find one or both locations"
            },
            status=400
        )

    route = get_osrm_route(
        start_coords,
        end_coords
    )

    if not route:
        return Response(
            {
                "error":
                "Unable to generate route"
            },
            status=400
        )

    distance = (
        route["distance"] / 1609.34
    )

    route_geometry = (
        route["geometry"]["coordinates"]
    )

    vehicle_range = VEHICLE_RANGE

    required_fuel_stops = max(
        0,
        math.ceil(
            distance / vehicle_range
        ) - 1
    )

    checkpoints = get_route_checkpoints(
        route_geometry,
        distance,
        vehicle_range
    )

    avg_price = (
        FuelStation.objects.aggregate(
            Avg("retail_price")
        )["retail_price__avg"]
        or 0
    )

    fuel_needed = (
        distance / VEHICLE_MPG
    )

    estimated_cost = (
        fuel_needed *
        avg_price
    )

    highest_price = (
        FuelStation.objects.aggregate(
            Max("retail_price")
        )["retail_price__max"]
        or avg_price
    )

    worst_case_cost = (
        fuel_needed *
        highest_price
    )

    estimated_savings = (
        worst_case_cost -
        estimated_cost
    )

    fuel_stops = []

    for stop_number, checkpoint in enumerate(
        checkpoints,
        start=1
    ):

        checkpoint_coords = (
            checkpoint[1],
            checkpoint[0]
        )

        nearby = []

        nearby_stations = FuelStation.objects.filter(
            latitude__gte=checkpoint_coords[0] - 2,
            latitude__lte=checkpoint_coords[0] + 2,
            longitude__gte=checkpoint_coords[1] - 2,
            longitude__lte=checkpoint_coords[1] + 2
        )

        for station in nearby_stations:

            station_coords = (
                station.latitude,
                station.longitude
            )

            miles_from_checkpoint = (
                distance_from_point(
                    checkpoint_coords,
                    station_coords
                )
            )

            if miles_from_checkpoint <= MAX_STATION_DISTANCE:

                nearby.append({

                    "truckstop_name":
                    station.truckstop_name,

                    "city":
                    station.city.strip(),

                    "state":
                    station.state,

                    "retail_price":
                    round(
                        station.retail_price,
                        3
                    ),

                    "distance_from_checkpoint":
                    round(
                        miles_from_checkpoint,
                        2
                    )
                })

        nearby = sorted(
            nearby,
            key=lambda x: (
                x["retail_price"],
                x["distance_from_checkpoint"]
            )
        )

        if nearby:

            fuel_stops.append({

                "stop_number":
                stop_number,

                "recommended_station":
                nearby[0],

                "alternative_stations":
                nearby[1:4]
            })

        else:

            fuel_stops.append({

                "stop_number":
                stop_number,

                "message":
                "No fuel station found within 100 miles"
            })

    execution_time = round(
        time.time() - start_time,
        3
    )

    map_url = (
        f"https://www.google.com/maps/dir/"
        f"{start}/{end}"
    )

    response_data = {

        "project":
        "FuelData Engine",

        "version":
        "1.0.0",

        "execution_time_seconds":
        execution_time,

        "route_summary": {

            "start":
            start,

            "destination":
            end,

            "distance_miles":
            round(distance, 2),

            "estimated_drive_hours":
            round(
                route["duration"] / 3600,
                2
            )
        },

        "routing_engine":
        "OSRM",

        "distance_miles":
        round(distance, 2),

        "estimated_drive_hours":
        round(
            route["duration"] / 3600,
            2
        ),

        "vehicle_range":
        vehicle_range,

        "required_fuel_stops":
        required_fuel_stops,

        "fuel_needed":
        round(
            fuel_needed,
            2
        ),

        "estimated_cost":
        round(
            estimated_cost,
            2
        ),

        "estimated_savings":
        round(
            estimated_savings,
            2
        ),

        "route_points":
        len(route_geometry),

        "map_url":
        map_url,

        "fuel_stops":
        fuel_stops,

        "assumptions": {

            "vehicle_mpg":
            VEHICLE_MPG,

            "vehicle_range_miles":
            VEHICLE_RANGE
        }
    }

    cache.set(
        cache_key,
        response_data,
        timeout=3600
    )

    return Response(
        response_data
    )

def cheapest_states(request):

    limit = int(
        request.GET.get(
            "limit",
            5
        )
    )

    states = (
        FuelStation.objects
        .values("state")
        .annotate(
            average_price=Avg(
                "retail_price"
            )
        )
        .order_by("average_price")[:limit]
    )

    data = []

    for state in states:

        data.append({

            "state":
            state["state"],

            "average_price":
            round(
                state["average_price"],
                3
            )
        })

    return JsonResponse(
        data,
        safe=False
    )



def home(request):

    total_stations = FuelStation.objects.count()

    avg_price = (
        FuelStation.objects.aggregate(
            Avg("retail_price")
        )["retail_price__avg"]
        or 0
    )

    total_states = (
        FuelStation.objects.values(
            "state"
        ).distinct().count()
    )

    context = {
        "total_stations": total_stations,
        "avg_price": round(avg_price, 2),
        "total_states": total_states,
    }

    return render(
        request,
        "home.html",
        context
    )




from django.http import JsonResponse
from django.db.models import Avg

def most_expensive_states(request):

    data = (
        FuelStation.objects
        .values("state")
        .annotate(
            average_price=Avg("retail_price")
        )
        .order_by("-average_price")[:10]
    )

    return JsonResponse(
        list(data),
        safe=False
    )