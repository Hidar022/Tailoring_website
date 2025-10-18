from django.urls import path
from . import views

urlpatterns = [
    path('create-admin/', views.create_admin, name='create_admin'),

    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Measurements
    path('add-measurements/', views.add_measurements, name='add_measurements'),
    path('my-measurements/', views.my_measurements, name='my_measurements'),
    path('edit-measurement/<int:measurement_id>/', views.edit_measurement, name='edit_measurement'),

    # Orders
    path('order/<int:product_id>/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]

