from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from.forms import ProductForm, ReviewForm,VariationForm
from .models import Product, ProductGallery, Variation
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from. models import ReviewandRating
from django.contrib import messages
from orders.models import OrderProduct
from accounts.forms import UserProfile,UserForm

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        # product_count = products.count()
    context = {
        "products": products,
        #'product_count': product_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()

    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
            
        except OrderProduct.DoesNotExist:
            order_product = None
            
        else:
            order_product = None
        
    reviews = ReviewandRating.objects.filter(product_id=single_product.id,status=True)
    
    # Get the Product Gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "reviews" : reviews,
        # "order_product" : order_product,
        'product_gallery' : product_gallery,
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
        context = {
            "products": products,
        }
    return render(request, "store/store.html", context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewandRating.objects.get(user__id=request.user.id,product__id=product_id,)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you! The review has been updated.')
            return redirect(url)
            
        except ReviewandRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewandRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you! The review has been submitted.')
                return redirect(url)
            
            #<-- Admin View Starts here -->
            
# Add product through Admin panel
@login_required(login_url="login")
def admin_dashboard(request):
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'userprofile' : userprofile,
    }
   
    return render(request,'admin/admin_dashboard.html',context)

# View product list
@login_required(login_url="login")
def view_product(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        # product_count = products.count()
    context = {
        "products": products,
        #'product_count': product_count,
    }
    
    return render(request,'admin/view_product.html',context)

# Add new Product
@login_required(login_url="login")
def add_product(request):
       if request.method == "POST":
            product_form = ProductForm(request.POST,request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, "New Product added Successfully.")
                return redirect(add_product)
            else:
                return HttpResponse('Error')       
       else:
        product_form = ProductForm()
        context = {
            "product_form" : product_form,
        }
        return render(request,'admin/add_product.html',context)
    
    # Delete product from database
@login_required(login_url="login")
def delete_product(request,slug):
    product = Product.objects.get(slug=slug)
    product.delete()
    messages.success(request,'Product deleted Successfully')
    return redirect(view_product)
    
    
    
# View Variation list in admin panel
@login_required(login_url="login")
def view_variation(request):
    variations = Variation.objects.all().filter()
    
    context = {
        'variations' : variations,
    }
    return render(request,'admin/view_variation.html',context)

# View Reviews and Ratings in admin panel
@login_required(login_url="login")
def view_review(request):
    reviews = ReviewandRating.objects.all().filter()
    
    context = {
        'reviews' : reviews,
    }
    return render(request,'admin/view_review.html',context)

# Add Variation from admin panel
@login_required(login_url="login")
def add_variation(request):
     if request.method == "POST":
            variation_form = VariationForm(request.POST)
            if variation_form.is_valid():
                variation_form.save()
                messages.success(request, "New Variation added Successfully.")
                return redirect(add_variation)
            else:
                return HttpResponse('Error')       
     else:
        variation_form = VariationForm()
        context = {
            "variation_form" : variation_form,
        }
     return render(request,'admin/add_variation.html',context)
 
#  Delete Variation
@login_required(login_url="login")
def delete_variation(request,id):
    variation = Variation.objects.get(id=id)
    variation.delete()
    messages.success(request,'Variation deleted Successfully.')
    return redirect(view_variation)