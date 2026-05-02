from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import ClientProfile, Membership

# Unregister only Group to simplify the admin interface
admin.site.unregister(Group)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'user_email', 'phone_number', 'membership_status', 'created_at')
    search_fields = ('client_name', 'phone_number', 'user__email')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def membership_status(self, obj):
        # Retrieve the latest membership based on end_date (ordered in models.py)
        latest_membership = obj.user.memberships.first()
        if latest_membership:
            status = latest_membership.payment_status
            # Add some visual distinction based on status if desired, though simple text works
            return f"{status} ({latest_membership.membership_type})"
        return "No Active Membership"
    membership_status.short_description = 'Membership Status'

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'start_date', 'end_date', 'payment_status')
    list_filter = ('membership_type', 'payment_status')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    
    def has_add_permission(self, request):
        return False
