from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, Measurement


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
    )
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__email', 'product__name')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


# =============================
#   OTHER MODELS
# =============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'height', 'date_added')
    search_fields = ('user__username', 'gender')
    list_filter = ('gender',)
