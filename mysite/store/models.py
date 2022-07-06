from distutils.command.upload import upload
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from category.models import Category
from django.urls import reverse
from django.db.models import Avg,Count
from accounts.models import Account

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    def average_review(self):
        reviews = ReviewandRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews ['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count(self):
        reviews = ReviewandRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews ['count'] is not None:
            count = int(reviews['count'])
        return count
        


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(
            variation_category="color", is_active=True
        )


variation_category_choice = (("color", "color"),)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewandRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products',max_length=255)
    
    class Meta:
        verbose_name = "product gallery"
        verbose_name_plural = "product gallery"
    
    def __str__(self):
        return self.product.product_name
    
    
# class Wishlist(models.Model):
#     user = models.ForeignKey(Account,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     slug = models.CharField(max_length=30,null=True,blank=True)
#     added_date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.user.email
    
    
    

    