from django.urls import path

from .views import (
    health_check,
    fuel_stations,
    cheapest_stations,
    station_stats,
    route_cost,
    route_optimizer,
    route_planner,
    state_prices,
    cheapest_states,
    most_expensive_states,
    
)

urlpatterns = [
    path('health/', health_check),
    path('fuel-stations/', fuel_stations),
    path('cheapest-stations/', cheapest_stations),
    path('station-stats/', station_stats),
    path('route-cost/', route_cost),
    path('route-optimizer/', route_optimizer),
    path('route-planner/', route_planner),
    path('state-prices/', state_prices),
    path('cheapest-states/', cheapest_states),
    path('most-expensive-states/',most_expensive_states),

]