from django.urls import path

from .views import (
    health_check,
    fuel_stations,
    cheapest_stations,
    station_stats,
    route_cost,
    route_optimizer,
)

urlpatterns = [
    path('health/', health_check),
    path('fuel-stations/', fuel_stations),
    path('cheapest-stations/', cheapest_stations),
    path('station-stats/', station_stats),
    path('route-cost/', route_cost),
    path('route-optimizer/', route_optimizer),
]