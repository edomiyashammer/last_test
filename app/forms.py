# products/forms.py
from django import forms
from .models import Product


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             "title",
#             "category",
#             "subcategory",
#             "description",
#             "price",
#             "information",
#             "image1",
#             "color",
#             "location",
#         ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to each form field widget
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
