from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import F
from django.urls import reverse
from django.utils.text import slugify

from users.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=50)
    imagecat = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name


class Product(models.Model):

    # Add the 'is_featured' field
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None )  # Set default value to None or a specific user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey("Subcategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=50)
    product_type = models.CharField(max_length=50)
    quantite = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    information = models.TextField(max_length=100)
    review = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to="products/")
    image2 = models.ImageField(upload_to="products/", blank=True, null=True)
    image3 = models.ImageField(upload_to="products/", blank=True, null=True)
    image4 = models.ImageField(upload_to="products/", blank=True, null=True)
    image5 = models.ImageField(upload_to="products/", blank=True, null=True)
    location = models.CharField(max_length=50)
    videolink = models.CharField(max_length=100)
    sizes = models.CharField(max_length=50, blank=True)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_featured = models.BooleanField(default=False)


def product_list(request, sale=False):
    products = Product.objects.all()

    if sale:
        # Filter for sale products (discounted price is not null)
        products = products.filter(discount_price__isnull=False)

    # Filter by price range
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))

    # Filter by size
    selected_size = request.GET.get("size")
    if selected_size:
        products = products.filter(sizes__contains=selected_size)

    # Retrieve the latest products
    latest_products = Product.objects.order_by("-id")[:5]

    return render(
        request,
        "product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "latest_products": latest_products,
            "sale": sale,
        },
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add user profile fields (e.g., address, phone number, etc.)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    # Add order-related fields (e.g., shipping address, payment details, order status)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )
    comment = models.TextField()


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    imagesub = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=50)
    product_type = models.CharField(max_length=50)
    quantite = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    information = models.TextField(max_length=100)
    review = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to="products/")
    image2 = models.ImageField(upload_to="products/", blank=True, null=True)
    image3 = models.ImageField(upload_to="products/", blank=True, null=True)
    image4 = models.ImageField(upload_to="products/", blank=True, null=True)
    image5 = models.ImageField(upload_to="products/", blank=True, null=True)
    location = models.CharField(max_length=50)
    videolink = models.CharField(max_length=100)
    sizes = models.CharField(max_length=50, blank=True)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
