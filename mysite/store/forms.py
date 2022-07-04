from dataclasses import fields
from tkinter import Widget
from django import forms
from . models import ReviewandRating,Product,Variation

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewandRating
        fields = ['subject','review','rating']
        
        
class ProductForm(forms.ModelForm):
    # images = forms.ImageField(required=True,error_messages = {'Invalid':{"Image files only"}},widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name','slug','description','price','stock','is_available','category','images']
        

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product','variation_category','variation_value','is_active']