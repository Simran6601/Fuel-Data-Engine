from django.db import models

class FuelStation(models.Model):

    truckstop_name = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=50)

    retail_price = models.FloatField()

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    class Meta:

        indexes = [

            models.Index(
                fields=["state"]
            ),

            models.Index(
                fields=["city"]
            ),

            models.Index(
                fields=["retail_price"]
            ),

        ]

    def __str__(self):

        return (
            f"{self.truckstop_name}"
            f" ({self.city})"
        )