from django.contrib import admin
from .models import Member, SquadMembership


class SquadMembershipInline(admin.TabularInline):
    model = SquadMembership
    extra = 0


class MemberAdmin(admin.ModelAdmin):
    model = Member
    inlines = (SquadMembershipInline,)
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position')
    list_display = ('__unicode__', 'user', 'gender', 'pref_position', 'is_current')


class SquadMembershipAdmin(admin.ModelAdmin):
    model = SquadMembership
    search_fields = ('member',)
    list_filter = ('member', 'team', 'season')
    list_display = ('__unicode__', 'member', 'team', 'season')


# Register all members models with the admin interface
admin.site.register(Member, MemberAdmin)
admin.site.register(SquadMembership, SquadMembershipAdmin)
