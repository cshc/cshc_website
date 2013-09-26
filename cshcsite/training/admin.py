from django.contrib import admin
from .models import TrainingSession


class TrainingSessionAdmin(admin.ModelAdmin):
    """Admin interface for a training session"""
    list_display = ('__unicode__', 'description', 'venue', 'datetime', 'duration_mins')


# Register all training models with the admin interface
admin.site.register(TrainingSession, TrainingSessionAdmin)