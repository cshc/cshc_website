""" Configuration of training models for the Django admin interface.
"""

from django.contrib import admin
from training.models import TrainingSession


class TrainingSessionAdmin(admin.ModelAdmin):
    """Admin interface for a training session"""
    search_fields = ('venue__name', 'description')
    list_filter = ('venue',)
    list_display = ('__unicode__', 'description', 'venue', 'datetime', 'duration_mins')


# Register all training models with the admin interface
admin.site.register(TrainingSession, TrainingSessionAdmin)
