from django import forms
from .models import Home_Banner, Brand


class Home_BannerForm(forms.ModelForm):
    class Meta:
        model = Home_Banner
        fields = '__all__'


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'
