from django.contrib import admin
from .models import Request, Service

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'contact_info', 'service', 'preferred_date_time', 'payment_type', 'status')
    list_filter = ('user', 'service', 'preferred_date_time', 'payment_type', 'status')
    search_fields = ('user__username', 'address', 'contact_info', 'service__name', 'preferred_date_time', 'payment_type', 'status')

    fieldsets = (
        (None, {
            'fields': ('user', 'address', 'contact_info', 'service', 'preferred_date_time', 'payment_type', 'status', 'cancellation_reason')
        }),
    )

admin.site.register(Request, RequestAdmin)
admin.site.register(Service)
