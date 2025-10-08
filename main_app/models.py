from django.db import models
from django.contrib.auth.models import User


# ================================
#   PRODUCT MODEL
# ================================
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


# ================================
#   ORDER MODEL
# ================================
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"


# ================================
#   PROFILE MODEL
# ================================
class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BODY_TYPE_CHOICES = [
        ('Slim', 'Slim'),
        ('Average', 'Average'),
        ('Plus Size', 'Plus Size'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True, null=True)
    favorite_style = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


# ================================
#   MEASUREMENT MODEL
# ================================
class Measurement(models.Model):
    GENDER_CHOICES = [
        ('male', "Men's"),
        ('female', "Women's"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')

    height = models.FloatField(help_text="Full body height")
    chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)
    arm_length = models.FloatField(null=True, blank=True)

    bust = models.FloatField(null=True, blank=True)
    shoulder = models.FloatField(null=True, blank=True)
    hand = models.FloatField(null=True, blank=True)
    shirt_length = models.FloatField(null=True, blank=True)
    trouser_length = models.FloatField(null=True, blank=True)
    neck_size = models.FloatField(null=True, blank=True)
    shirt_size = models.FloatField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.gender} measurement ({self.date_added.date()})"
