from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FuelStation


# --------------------------------------------------
# Admin Branding
# --------------------------------------------------

admin.site.site_header = "FuelData Engine Administration"
admin.site.site_title = "FuelData Engine"
admin.site.index_title = "Fleet Route Optimization Dashboard"
admin.site.enable_nav_sidebar = True


# --------------------------------------------------
# Remove Groups (not needed for this assignment)
# --------------------------------------------------

admin.site.unregister(Group)


# --------------------------------------------------
# Fuel Station Admin
# --------------------------------------------------

@admin.register(FuelStation)
class FuelStationAdmin(admin.ModelAdmin):

    list_display = (
        "truckstop_name",
        "city",
        "state",
        "retail_price",
        "latitude",
        "longitude",
    )

    search_fields = (
        "truckstop_name",
        "city",
        "state",
    )

    list_filter = (
        "state",
    )

    ordering = (
        "retail_price",
    )

    list_per_page = 50

    save_on_top = True

    list_display_links = (
        "truckstop_name",
    )

    list_editable = (
        "retail_price",
    )

    list_filter = (
    "state",
)

search_fields = (
    "truckstop_name",
    "city",
    "state",
)

list_per_page = 50

ordering = (
    "retail_price",
)

readonly_fields = (
    "retail_price",
)

admin.site.site_header = (
    "FuelData Engine"
)

admin.site.site_title = (
    "FuelData Admin"
)

admin.site.index_title = (
    "Fleet Route Optimization Dashboard"
)