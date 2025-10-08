from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, Measurement, Profile


# =============================
#   ORDER ADMIN CONFIGURATION
# =============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'get_email',
        'product',
        'quantity',
        'status',
        'order_date',
        'view_profile',
    )
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
            return format_html(
                '<a href="/admin/main_app/profile/{}/change/" style="color:blue;">View Profile</a>',
                obj.user.profile.id
            )
        return "-"
    view_profile.short_description = "Profile"


# =============================
#   PROFILE ADMIN CONFIGURATION
# =============================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'profile_image',
        'user',
        'full_name',
        'phone',
        'gender',
        'body_type',
        'city',
        'state',
        'country',
        'view_orders',
    )
    search_fields = ('user__username', 'full_name', 'phone', 'city', 'state', 'country')
    list_filter = ('gender', 'body_type', 'country')

    def profile_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">', obj.profile_picture.url)
        return "No Image"
    profile_image.short_description = 'Photo'

    def view_orders(self, obj):
        return format_html(
            '<a href="/admin/main_app/order/?user__id__exact={}" style="color:green;">View Orders</a>',
            obj.user.id
        )
    view_orders.short_description = "Orders"


# =============================
#   OTHER MODELS
# =============================
admin.site.register(Product)
admin.site.register(Measurement)
