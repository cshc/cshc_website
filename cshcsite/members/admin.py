from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    model = Member
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position')
    list_display = ('first_name', 'last_name', 'gender', 'is_current')


# Register all members models with the admin interface
admin.site.register(Member, MemberAdmin)