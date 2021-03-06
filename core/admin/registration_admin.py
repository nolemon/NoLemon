from django.contrib.admin import ModelAdmin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from core.models import registration_models

__all__ = ['RegistrationAdmin']

class RegistrationAdmin(ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__email')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady activated.
        """
        for profile in queryset:
            registration_models.RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = "Activate users"

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.
        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already activated.
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = "Re-send activation emails"