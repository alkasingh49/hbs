from django.contrib import admin

from .models import Booking, Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'created_at')
    list_filter = ('active', 'discount_percent')
    search_fields = ('code',)
    ordering = ('code',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'room',
        'user',
        'check_in',
        'check_out',
        'nights',
        'coupon',
        'discount_percent',
        'total_price',
    )
    list_filter = ('check_in', 'check_out', 'coupon')
    search_fields = ('room__room_number', 'user__username', 'coupon__code')
    readonly_fields = ('created_at',)
    date_hierarchy = 'check_in'

    @admin.display(ordering='check_in', description='Nights')
    def nights(self, obj):
        return obj.nights
