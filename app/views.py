from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ProductForm
from .models import Category, Product, Cart, CartItem, Subcategory, Post
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from PIL import Image, ImageDraw, ImageFont
from django.db.models.signals import post_save


def index(request, category_id=None):

    if category_id:
        # If a category is specified in the URL, filter products by that category
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        # If no category is specified, display all products
        category = None
        products = Product.objects.all()

    # Query for featured products
    featured_products = Product.objects.filter(is_featured=True)

    # Query for latest products
    latest_products = Product.objects.order_by("-id")[:5]

    # Query for all product categories
    categories = Category.objects.all()

    return render(
        request,
        "index.html",
        {
            "category_id": category_id,
            "category": category,
            "products": products,
            "featured_products": featured_products,
            "latest_products": latest_products,
            "categories": categories,
        },
    )


def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request, "category_detail.html", {"category": category, "products": products}
    )


def product_list(request):
    products = Product.objects.all()
    return render(request, "shopgrid.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shopdetails.html", {"product": product})


def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
    else:
        # Handle the case for unauthenticated users
        # You can use session or any other method to track the cart for unauthenticated users
        # For simplicity, let's use session for demonstration purposes
        cart_items = request.session.get("cart_items", [])

    if request.method == "POST":
        # Handle updating cart quantities for authenticated users
        if request.user.is_authenticated:
            for item in cart_items:
                new_quantity = request.POST.get(str(item.id))
                if new_quantity:
                    item.quantity = int(new_quantity)
                    item.save()

        # Handle applying discount code (you may need to adjust this logic)
        discount_code = request.POST.get("discount_code")
        # Implement code to apply the discount and update cart totals here

    return render(request, "cart.html", {"cart_items": cart_items})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            item.quantity += 1
            item.save()
    else:
        cart_items = request.session.get("cart_items", [])
        # Check if the item is already in the cart
        item = next(
            (item for item in cart_items if item["product_id"] == str(product_id)), None
        )
        if item:
            item["quantity"] += 1
        else:
            cart_items.append({"product_id": str(product_id), "quantity": 1})
        request.session["cart_items"] = cart_items

    return redirect("cart")


@login_required
def checkout(request):
    if request.method == "POST":
        # Handle the form submission if needed

        # Get cart items for authenticated users or from session for unauthenticated users
        if request.user.is_authenticated:
            user = request.user
            cart_items = CartItem.objects.filter(user=user)
        else:
            # For simplicity, use session to store cart items for unauthenticated users
            cart_items = request.session.get("cart_items", [])

        # Ensure cart_items is always a list
        if not isinstance(cart_items, list):
            cart_items = []

        # Calculate total price of all cart items
        total_price = sum(item["price"] * item["quantity"] for item in cart_items)

        # Initialize products as an empty list
        products = []

        # Check if cart_items is not empty before creating the products list
        if cart_items:
            products = [
                {
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": item["quantity"],
                }
                for item in cart_items
            ]

    return render(request, "checkout.html", {"total_price": total_price})


def contact(request):

    return render(request, "contact.html")

    return render(request, "cat.html")


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "category_list.html", {"categories": categories})


class SubcategoryListView(View):
    template_name = "subcategory_list.html"

    def get(self, request, category_id=None):
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            subcategories = Subcategory.objects.filter(category=category)
        else:
            subcategories = Subcategory.objects.all()

        context = {"subcategories": subcategories, "category": category}
        return render(request, self.template_name, context)


class ProductListView(View):
    template_name = "product_list.html"

    def get(self, request, subcategory_id=None):
        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            products = Product.objects.filter(subcategory=subcategory)
        else:
            products = Product.objects.all()

        context = {"products": products}
        return render(request, self.template_name, context)


class ProductListView(View):
    template_name = "product_list.html"

    def get(self, request, category_id=None, subcategory_id=None):
        products = Product.objects.all()

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            products = products.filter(subcategory__category=category)

        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            products = products.filter(subcategory=subcategory)

        context = {"products": products}
        return render(request, self.template_name, context)


def trend(request):
    products = Product.objects.all()
    return render(request, "trand.html", {"products": products})


@receiver(post_save, sender=Product)
def add_watermark(sender, instance, created, **kwargs):
    if created:  # Only perform this action if the product is newly created
        watermark_path = "assets/assets/img/WaterMark.png"
        product_image_path = (
            instance.image1.path
        )  # Assuming image1 is the main product image

        # Open the product image
        with Image.open(product_image_path) as img:
            # Open the watermark image
            with Image.open(watermark_path) as watermark:
                # Calculate the position to place the watermark at the center
                position = (
                    (img.width - watermark.width) // 2,
                    (img.height - watermark.height) // 2,
                )

                # Paste the watermark onto the product image
                img.paste(watermark, position, watermark)

                # Save the modified image
                img.save(product_image_path)


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")  # Redirect to home page after successful submission
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("/")  # Redirect to "my_ads" after successful edit
    else:
        form = ProductForm(instance=product)
    return render(request, "product_edit.html", {"form": form, "product": product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("Profile")  # Redirect to "my_ads" after successful deletion
    return render(request, "product_confirm_delete.html", {"product": product})


@login_required
def success(request):
    return render(request, "success.html")


@login_required
def Dash(request):

    products = Product.objects.all()

    return render(request, "dashboard.html", {'products': products})


@login_required
def Profile(request):
    return render(request, "profile.html")


@login_required
def Privacy(request):
    return render(request, "privacy-setting.html")


@login_required
def my_ads(request):

    products = Product.objects.all()

    return render(request, "account-myads.html", {"products": products})


@login_required
def payment(request):
    return render(request, "payments.html")
