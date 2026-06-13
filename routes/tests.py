from django.test import TestCase, Client


class FuelApiTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_health_check(self):

        response = self.client.get(
            "/api/health/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_health_response_content(self):

        response = self.client.get(
            "/api/health/"
        )

        self.assertEqual(
            response.json()["status"],
            "healthy"
        )

    def test_station_stats(self):

        response = self.client.get(
            "/api/station-stats/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_station_stats_response(self):

        response = self.client.get(
            "/api/station-stats/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_route_cost_valid(self):

        response = self.client.get(
            "/api/route-cost/?distance=1000&mileage=10"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_route_cost_invalid_mileage(self):

        response = self.client.get(
            "/api/route-cost/?distance=1000&mileage=0"
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_route_cost_invalid_distance(self):

        response = self.client.get(
            "/api/route-cost/?distance=-100&mileage=10"
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_route_optimizer_invalid_mileage(self):

        response = self.client.get(
            "/api/route-optimizer/?distance=1000&mileage=0&tank_capacity=100"
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_route_optimizer_invalid_tank(self):

        response = self.client.get(
            "/api/route-optimizer/?distance=1000&mileage=10&tank_capacity=0"
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_fuel_stations_pagination(self):

        response = self.client.get(
            "/api/fuel-stations/?page=1&page_size=10"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_fuel_stations_page_two(self):

        response = self.client.get(
            "/api/fuel-stations/?page=2&page_size=10"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_cheapest_stations(self):

        response = self.client.get(
            "/api/cheapest-stations/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_state_prices(self):

        response = self.client.get(
            "/api/state-prices/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_cheapest_states(self):

        response = self.client.get(
            "/api/cheapest-states/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_route_planner_missing_params(self):

        response = self.client.get(
            "/api/route-planner/"
        )

        self.assertEqual(
            response.status_code,
            400
        )