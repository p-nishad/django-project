from django.http import HttpResponse
from django.shortcuts import render,redirect
from. models import Category
from. forms import CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def view_category(request):
    categories = Category.objects.all().filter()
    
    context = {
        'categories' :categories,
    }
    return render(request,'admin/view_category.html',context)

# Add category
@login_required(login_url="login")
def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST,request.FILES)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,'New Category added Successfully.')
            return redirect(add_category)
        else:
            HttpResponse('Error')
    else:
        category_form = CategoryForm()
        
        context = {
            'category_form' : category_form,
        }
    return render(request,'admin/add_category.html',context)

# @login_required(login_url="login")
# def delete_category(request,slug):
#         category = Category.objects.get(slug=slug)
#         category.delete()
#         messages.success(request,'Category deleted Successfully.')
#         return redirect(delete_category)