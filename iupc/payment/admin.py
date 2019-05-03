from django.contrib import admin

# Register your models here.
from payment.models import PaymentStatus


class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'university', 'status')


admin.site.register(PaymentStatus, PaymentStatusAdmin)