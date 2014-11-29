""" Configuration of Members models for the admin interface.
"""

from django.contrib import admin
from members.models import Member, SquadMembership, CommitteeMembership, CommitteePosition


class SquadMembershipInline(admin.TabularInline):
    """ Allows squad membership to be edited from the admin page of the member model."""
    model = SquadMembership
    extra = 0


class MemberAdmin(admin.ModelAdmin):
    """ Admin interface definition for the Member model."""
    model = Member
    inlines = (SquadMembershipInline,)
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position')
    list_display = ('__unicode__', 'user', 'gender', 'pref_position', 'is_current')


class SquadMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the SquadMembership model."""
    model = SquadMembership
    search_fields = ('member__firstname', 'member__lastname')
    list_filter = ('member', 'team', 'season')
    list_display = ('__unicode__', 'member', 'team', 'season')


class CommitteePositionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteePosition model."""
    model = CommitteePosition
    search_fields = ('name',)
    list_filter = ('name', 'gender')
    list_display = ('__unicode__', 'name', 'gender')


class CommitteeMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteeMembership model."""
    model = CommitteeMembership
    search_fields = ('member__firstname', 'member__lastname')
    list_filter = ('member', 'position', 'season')
    list_display = ('__unicode__', 'member', 'position', 'season')


# Register all members models with the admin interface
admin.site.register(Member, MemberAdmin)
admin.site.register(SquadMembership, SquadMembershipAdmin)
admin.site.register(CommitteeMembership, CommitteeMembershipAdmin)
admin.site.register(CommitteePosition, CommitteePositionAdmin)
