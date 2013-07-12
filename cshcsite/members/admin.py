from django.contrib import admin
from .models import Member, MembershipEnquiry

# Register all members models with the admin interface
admin.site.register(Member)
admin.site.register(MembershipEnquiry)

