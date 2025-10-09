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
