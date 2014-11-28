""" Configuration of Venues models for the Django admin interface.
"""

from django.contrib import admin
from venues.models import Venue


class VenueAdmin(admin.ModelAdmin):
    """Admin interface definition for the Venue model"""
    readonly_fields = ('slug',)
    search_fields = ('name',)
    list_filter = ('is_home',)
    list_display = ('name', 'short_name', 'url', 'is_home')


# Register all venues models with the admin interface
admin.site.register(Venue, VenueAdmin)
