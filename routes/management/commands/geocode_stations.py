from django.core.management.base import BaseCommand
from routes.models import FuelStation
from geopy.geocoders import Nominatim
import time


class Command(BaseCommand):

    help = "Add latitude and longitude to stations"

    def handle(self, *args, **kwargs):

        geolocator = Nominatim(user_agent="fueldata_engine")

        stations = FuelStation.objects.filter(
            latitude__isnull=True
        )

        updated = 0

        for station in stations:

            try:

                location = geolocator.geocode(
                    f"{station.city}, {station.state}, USA"
                )

                if location:

                    station.latitude = location.latitude
                    station.longitude = location.longitude
                    station.save()

                    updated += 1

                    self.stdout.write(
                        f"Updated: {station.city}, {station.state}"
                    )

                time.sleep(1)

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(str(e))
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} stations."
            )
        )