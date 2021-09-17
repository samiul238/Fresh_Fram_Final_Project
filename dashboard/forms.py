from django import forms
from products.models import *


class Addcat_Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = '__all__'


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'sub_category', 'name', 'unit', 'image',
                  'product_id', 'description', 'tags', 'brand',
                  'price', 'discount_price', 'count_in_stock', 'include', 'video', 'certificate'
                  ]

        widgets = {
            # 'category': forms.TextInput(attrs={'class': 'form-control', 'id': 'categoryid'}),
            # 'sub_category': forms.CheckboxSelectMultiple(attrs={'class': 'product-sub_category', 'id': 'sub_categoryid'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'nameid'}),
            # 'unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'unitid'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'imageid'}),
            'product_id': forms.TextInput(attrs={'class': 'form-control', 'id': 'product_id'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'descriptionid', 'style': 'height: 300px;'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'id': 'tagsid'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'id': 'brandid'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'priceid'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount_priceid'}),
            'count_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'count_in_stockid'}),
            # 'include': forms.Textarea(attrs={'class': 'form-control', 'id': 'includeid'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'id': 'videoid'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control', 'id': 'certificateid'}),
        }
