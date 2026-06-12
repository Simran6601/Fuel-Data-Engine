import pandas as pd

from django.core.management.base import BaseCommand
from routes.models import FuelStation


class Command(BaseCommand):

    help = "Import fuel station data"

    def handle(self, *args, **kwargs):

        csv_path = "data/fuel-prices-for-be-assessment.csv"

        df = pd.read_csv(csv_path)

        imported = 0

        for _, row in df.iterrows():

            FuelStation.objects.create(
                truckstop_name=row["Truckstop Name"],
                city=row["City"],
                state=row["State"],
                retail_price=row["Retail Price"]
            )

            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported} fuel stations."
            )
        )