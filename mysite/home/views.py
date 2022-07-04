from django.shortcuts import render
from store.models import Product
from store.views import ReviewandRating

# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    
    for product in products:
        reviews = ReviewandRating.objects.filter(product_id=product.id,status=True)
    reviews = 0

    context = {
        'products': products,
        'reviews' : reviews,
    }
    return render(request,'home.html',context)

