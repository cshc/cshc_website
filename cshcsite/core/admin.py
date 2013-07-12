from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from .forms import FlatPageForm
from .models import ClubInfo

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    """Override for the FlatPage admin interface - uses a TinyMCE widget"""

    form = FlatPageForm
    fieldsets = [
        ('None', {'fields': ['url', 'title', 'sites']}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),

        ('Content', {
            'classes': ('full-width',),  
            'fields': ['content']}),
    ]


class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


# Re-register the FlatPage admin interface
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)
admin.site.register(ClubInfo, ClubInfoAdmin)