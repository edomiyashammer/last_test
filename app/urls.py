from django.urls import path


from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("trend", views.trend, name="trend"),
    path("Dashboard/", views.Dash, name="Dash"),
    path("Privacy/", views.Privacy, name="Privacy"),
    path("my_ads/", views.my_ads, name="my_ads"),
    path("edit/<int:pk>/", views.product_edit, name="product_edit"),
    path("delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("Profile/", views.Profile, name="Profile"),
    path("payment/", views.payment, name="payment"),
    path("shopgrid", views.product_list, name="shopgrid"),
    path("success/", views.success, name="success"),
    path("shopdetails/<int:product_id>/", views.product_detail, name="product_detail"),
    path("create/", views.product_create, name="product_create"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact", views.contact, name="contact"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "subcategories/", views.SubcategoryListView.as_view(), name="subcategory-list"
    ),
    path(
        "subcategories/<int:category_id>/",
        views.SubcategoryListView.as_view(),
        name="subcategory-list-with-category",
    ),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:category_id>/<int:subcategory_id>/",
        views.ProductListView.as_view(),
        name="product-list-with-category-subcategory",
    ),
]
