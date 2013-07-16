from django.contrib import admin
from .models import Venue


class VenueAdmin(admin.ModelAdmin):
    """Admin interface for the Venue model"""
    readonly_fields = ('slug',)
    search_fields = ('name',)
    list_filter = ('is_home',)
    list_display = ('name', 'short_name', 'url', 'is_home')

# Register all venues models with the admin interface
admin.site.register(Venue, VenueAdmin)
