from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Measurement, ContactMessage


# -----------------------
# Home page
# -----------------------
def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


# -----------------------
# User Registration
# -----------------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if password1 != password2:
            messages.error(request, "Passwords do not match ❌")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken ❌")
            return redirect("register")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully ✅")
        return redirect("login")

    return render(request, "register.html")


# -----------------------
# User Login
# -----------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! ✅")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password ❌")
            return redirect("login")

    return render(request, "login.html")



# -----------------------
# User Logout
# -----------------------
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully ✅")
    return redirect("login")


# -----------------------
# About & Contact
# -----------------------
def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "✅ Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


# -----------------------
# Add or Edit Measurements
# -----------------------
@login_required
def add_measurements(request):
    if request.method == "POST":
        gender = request.POST.get("gender")

        measurement, created = Measurement.objects.get_or_create(user=request.user, gender=gender)

        measurement.height = request.POST.get("height")
        measurement.chest = request.POST.get("chest")
        measurement.waist = request.POST.get("waist")
        measurement.hips = request.POST.get("hips")
        measurement.arm_length = request.POST.get("arm_length")

        if gender == "female":
            measurement.bust = request.POST.get("bust")
            measurement.shoulder = None
            measurement.hand = None
            measurement.shirt_length = None
            measurement.trouser_length = None
            measurement.neck_size = None
            measurement.shirt_size = None
        else:
            measurement.shoulder = request.POST.get("shoulder")
            measurement.hand = request.POST.get("hand")
            measurement.shirt_length = request.POST.get("shirt_length")
            measurement.trouser_length = request.POST.get("trouser_length")
            measurement.neck_size = request.POST.get("neck_size")
            measurement.shirt_size = request.POST.get("shirt_size")
            measurement.bust = None

        measurement.save()

        if created:
            messages.success(request, f"{gender.capitalize()} measurement added successfully ✅")
        else:
            messages.success(request, f"{gender.capitalize()} measurement updated successfully ✅")

        return redirect(f"/my-measurements/?show={gender}")

    return render(request, "add_measurements.html")


@login_required
def my_measurements(request):
    female_measurements = Measurement.objects.filter(user=request.user, gender="female").order_by("-date_added")
    male_measurements = Measurement.objects.filter(user=request.user, gender="male").order_by("-date_added")
    show_gender = request.GET.get("show", None)

    context = {
        "female_measurements": female_measurements,
        "male_measurements": male_measurements,
        "show_gender": show_gender,
    }
    return render(request, "my_measurements.html", context)


@login_required
def edit_measurement(request, measurement_id):
    measurement = get_object_or_404(Measurement, id=measurement_id, user=request.user)

    if request.method == "POST":
        measurement.gender = request.POST.get("gender")
        measurement.height = request.POST.get("height")
        measurement.chest = request.POST.get("chest")
        measurement.waist = request.POST.get("waist")
        measurement.hips = request.POST.get("hips")
        measurement.arm_length = request.POST.get("arm_length")

        if measurement.gender == "female":
            measurement.bust = request.POST.get("bust")
            measurement.shoulder = None
            measurement.hand = None
            measurement.shirt_length = None
            measurement.trouser_length = None
            measurement.neck_size = None
            measurement.shirt_size = None
        else:
            measurement.shoulder = request.POST.get("shoulder")
            measurement.hand = request.POST.get("hand")
            measurement.shirt_length = request.POST.get("shirt_length")
            measurement.trouser_length = request.POST.get("trouser_length")
            measurement.neck_size = request.POST.get("neck_size")
            measurement.shirt_size = request.POST.get("shirt_size")
            measurement.bust = None

        measurement.save()
        messages.success(request, "Measurement updated successfully ✅")
        return redirect(f"/my-measurements/?show={measurement.gender}")

    return render(request, "edit_measurement.html", {"measurement": measurement})


# -----------------------
# Order Product
# -----------------------
@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
        )
        messages.success(request, f"Order placed successfully for {quantity} x {product.name} ✅")
        return redirect("my_orders")

    return render(request, "order.html", {"product": product})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-order_date")

    for order in orders:
        order.total_price = order.quantity * order.product.price

    return render(request, "my_orders.html", {"orders": orders})
