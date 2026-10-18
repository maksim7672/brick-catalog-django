from django.contrib import admin
from .models import Brick, Order

admin.site.register(Brick)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_phone', 'brick', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('client_name', 'client_phone')

