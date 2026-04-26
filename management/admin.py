from django.contrib import admin
from .models import ClientProfile, Membership

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user_fullname', 'user_email', 'phone_number', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number', 'user__email')

    def user_fullname(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_fullname.short_description = 'Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'start_date', 'end_date', 'payment_status')
    list_filter = ('membership_type', 'payment_status')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
