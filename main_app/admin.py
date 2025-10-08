from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, Measurement, Profile


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_email', 'product', 'quantity', 'status', 'order_date', 'view_profile')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__email', 'product__name')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def view_profile(self, obj):
        if hasattr(obj.user, 'profile'):
            return format_html('<a href="/admin/main_app/profile/{}/change/">View Profile</a>', obj.user.profile.id)
        return "-"
    view_profile.short_description = "Profile"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'full_name', 'phone', 'city', 'state', 'country', 'view_orders')
    search_fields = ('user__username', 'full_name', 'phone', 'city', 'state', 'country')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def view_orders(self, obj):
        return format_html('<a href="/admin/main_app/order/?user__id__exact={}">View Orders</a>', obj.user.id)
    view_orders.short_description = "Orders"


# Register other models normally
admin.site.register(Product)
admin.site.register(Measurement)
