from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Min, Max

from .models import FuelStation


def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "FuelData Engine"
    })


def fuel_stations(request):

    state = request.GET.get("state")
    city = request.GET.get("city")

    stations = FuelStation.objects.all()

    if state:
        stations = stations.filter(state=state.upper())

    if city:
        stations = stations.filter(city__icontains=city)

    stations = stations[:20]

    data = []

    for station in stations:
        data.append({
            "truckstop_name": station.truckstop_name,
            "city": station.city,
            "state": station.state,
            "retail_price": station.retail_price
        })

    return JsonResponse(data, safe=False)


def cheapest_stations(request):

    limit = int(request.GET.get("limit", 10))

    stations = FuelStation.objects.order_by("retail_price")[:limit]

    data = []

    for station in stations:
        data.append({
            "truckstop_name": station.truckstop_name,
            "city": station.city,
            "state": station.state,
            "retail_price": station.retail_price
        })

    return JsonResponse(data, safe=False)


def station_stats(request):

    stats = FuelStation.objects.aggregate(
        average_price=Avg("retail_price"),
        cheapest_price=Min("retail_price"),
        highest_price=Max("retail_price")
    )

    data = {
        "total_stations": FuelStation.objects.count(),
        "states_covered": FuelStation.objects.values("state").distinct().count(),
        "average_price": round(stats["average_price"], 3),
        "cheapest_price": stats["cheapest_price"],
        "highest_price": stats["highest_price"]
    }

    return JsonResponse(data)


@csrf_exempt
def route_cost(request):

    distance = float(request.GET.get("distance", 1200))
    mileage = float(request.GET.get("mileage", 10))

    avg_price = FuelStation.objects.aggregate(
        Avg("retail_price")
    )["retail_price__avg"]

    fuel_needed = distance / mileage

    estimated_cost = fuel_needed * avg_price

    return JsonResponse({
        "distance": distance,
        "mileage": mileage,
        "fuel_needed": round(fuel_needed, 2),
        "average_fuel_price": round(avg_price, 3),
        "estimated_cost": round(estimated_cost, 2)
    })


def route_optimizer(request):

    distance = float(request.GET.get("distance", 1200))
    mileage = float(request.GET.get("mileage", 10))
    tank_capacity = float(request.GET.get("tank_capacity", 100))

    fuel_needed = distance / mileage

    max_distance_per_tank = tank_capacity * mileage

    refuel_stops = int(fuel_needed // tank_capacity)

    avg_price = FuelStation.objects.aggregate(
        Avg("retail_price")
    )["retail_price__avg"]

    estimated_cost = fuel_needed * avg_price

    stations = FuelStation.objects.order_by(
        "retail_price"
    )[:5]

    recommended_stations = []

    for station in stations:
        recommended_stations.append({
            "truckstop_name": station.truckstop_name,
            "city": station.city,
            "state": station.state,
            "retail_price": station.retail_price
        })

    return JsonResponse({
        "distance": distance,
        "mileage": mileage,
        "tank_capacity": tank_capacity,
        "fuel_needed": round(fuel_needed, 2),
        "max_distance_per_tank": round(max_distance_per_tank, 2),
        "refuel_stops": refuel_stops,
        "estimated_cost": round(estimated_cost, 2),
        "recommended_stations": recommended_stations
    })