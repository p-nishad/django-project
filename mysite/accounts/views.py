from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import Order
from .forms import RegistrationForm, UserCreationForm,UserForm,UserProfileForm,AccountForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required,user_passes_test
from home.views import home
from store.views import admin_dashboard

# from. send_sms import sendsms
from .verify import check, send
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            request.session["phone_number"] = phone_number
            send(form.cleaned_data.get("phone_number"))
            user.save()

            messages.success(request, "Registration Successfull")
            return redirect("otp")
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)

def check_admin(user):
   return user.is_superuser

# @user_passes_test(check_admin)
def login(request):
    if 'user' in request.session:
        return redirect(home)
    elif 'admin' in request.session:
        return redirect(dashboard)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
                if user.is_superadmin:
                    request.session['admin'] = email
                    auth.login(request,user)
                    return redirect(admin_dashboard)
                # else:
                #     request.session['user'] = email
                #     auth.login(request,user)
                #     return redirect(home)
                    
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                        # Getting the product variation by cart_id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # Get the cart item from the user to access his product variation
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []

                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        # product_variation = [1,2,3,4,6]
                        # ex_var_list = [4,6,3,5]
                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass

                auth.login(request, user)
                messages.success(request, "You are logged in ")
                url = request.META.get("HTTP_REFERER")
                try:
                    query = requests.utils.urlparse(url).query

                    # next=/cart/checkout/
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        nextPage = params["next"]
                        return redirect(nextPage)

                except:
                    return redirect("home")

        else:
            messages.error(request, "Invalid login Credentials")
            return redirect("login")

    return render(request, "accounts/login.html")


# @login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


def activate(request, uidb64, token):
    return HttpResponse("Ok")


# @login_required(login_url="dashboard")
def dashboard(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id,is_ordered=True) 
    orders_count = orders.count()
    
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count' : orders_count,
        'userprofile' : userprofile,
    }
    return render(request, "accounts/dashboard.html",context)


def otp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")
            phone_number = request.session["phone_number"]
            if check(phone_number, code):
                user = Account.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()
                return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register_otp.html", {"form": form})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            # Reset password
            current_site = get_current_site(request)
            mail_subject = "Reset your Password"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, "Password reset email has been sent to your Email Address."
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exists.")
            return redirect("forgot_password")
    return render(request, "accounts/forgot_password.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExists):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password.")
        return redirect("reset_password")

    else:
        messages.error(request, "This link already expired.")
        return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfull.")
            return redirect("login")
        else:
            messages.error(request, "Password do not match")
            return redirect("reset_password")
    else:
        return render(request, "accounts/reset_password.html")
    
@login_required(login_url="login")    
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
    }
    return render(request,'accounts/my_orders.html',context)

@login_required(login_url="login")
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form =UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
            
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request,'Oops! Please enter valid Current Password')
                return redirect('change_password')
        else:
             messages.error(request,'Password does not match!') 
             return redirect('change_password') 
    return render(request,'accounts/change_password.html')


@login_required(login_url="login")
def order_detail(request, order_id):
    return render(request,'accounts/order_detail.html')

# View Accounts in admin panel
@login_required(login_url="login")
def view_account(request):
    accounts = Account.objects.all().filter()
    
    context = {
        'accounts' : accounts,
    }
    return render(request,'admin/view_account.html',context)

# Delete users in admin panel
def delete_user(request,id):
    account = Account.objects.get(id=id)
    account.delete()
    messages.success(request,'User deleted Successfully')
    return redirect(view_account)

@login_required(login_url="login")
def edit_admin_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile has been updated.')
            return redirect('edit_admin_profile')
    else:
        user_form =UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
            
    return render(request,'admin/edit_admin_profile.html',context)


# Add new User
def add_user(request):
    if request.method == 'POST':
        admin_form = AccountForm(request.POST)
        if admin_form.is_valid():
            admin_form.save()
            messages.success(request,'New User added Successfully')
            return redirect(add_user)
        else:
            return HttpResponse('Error')
        
    else:
        admin_form = AccountForm()
        context = {
            'admin_form' : admin_form,
        }
    return render(request,'admin/add_user.html',context)
