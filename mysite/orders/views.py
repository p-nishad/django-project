from datetime import datetime
from this import d
from django.http import HttpResponse
from django.shortcuts import render, redirect
from carts.models import CartItem
from accounts.views import my_orders
from store.models import Product
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from .forms import PaymentForm
import razorpay
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.
def payments(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    grand_total = 0
    shipping = 0
    total =0 
    quantity = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    shipping = (2 * total) / 100
    grand_total = total + shipping
    rz_total = int(grand_total) * 100

    # Create razorpay
    client = razorpay.Client(
        auth=("rzp_test_0DzMFV4V6t3o4d", "qbxeHpoL7mXP5ujLqP8pf4vu")
    )

    # Create order
    response_payment = client.order.create(dict(amount=rz_total, currency="INR"))

    order_id = response_payment["id"]
    order_status = response_payment["status"]
    if order_status == "created":
        payment = Payment(
            user=request.user,
            amount=rz_total,
            # order_id = order_id,
            razorpay_payment_id=order_id,
            paid=order_status,
        )
        # payment.paid = True
        payment.save()
        response_payment["user"] = current_user
    form = PaymentForm(request.POST or None)
    context = {"form": form, "payment": response_payment}
    
    # Move the cart items to order products table
    
    cart_items = CartItem.objects.filter(user=current_user)
    for item in cart_items:
        if payment.paid == "True":

            order_product = OrderProduct()
            order_product.order_id = response_payment["id"]
            order_product.payment = payment
            order_product.user_id = current_user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_id)
        order_product.variations.set(product_variation)
        order_product.save()

    # Send order email to customer
    mail_subject = "Thank You for your order"
    message = render_to_string(
        "accounts/order_recieved_email.html",
        {
            "user": request.user,
            # "orders" : order,
        },
    )

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and payment id back
    return render(request, "orders/payments.html", context)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count <= 0 ,redirect back to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    grand_total = 0
    shipping = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    shipping = (2 * total) / 100
    grand_total = total + shipping
    rz_total = int(grand_total) * 100

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all billing information inside the Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.shipping = shipping
            data.ip = request.META.get("REMOTE_ADDR")
            data.is_ordered = True
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 2022-6-14
            order_number = current_date + str(data.id)
            data.order_number = order_number
            # data.is_ordered = True
            data.save()

            client = razorpay.Client(
                auth=("rzp_test_0DzMFV4V6t3o4d", "qbxeHpoL7mXP5ujLqP8pf4vu")
            )

            # Create order
            response_payment = client.order.create(
                dict(amount=rz_total, currency="INR")
            )

            order_id = response_payment["id"]
            order_status = response_payment["status"]
            if order_status == "created":
                payment = Payment(
                    user=request.user,
                    amount=rz_total,
                    # order_id = order_id,
                    razorpay_payment_id=order_id,
                    # paid = order_status,
                )
                # payment.paid = True
                # payment.save()
                response_payment["user"] = current_user
            form = PaymentForm(request.POST or None)

            order = Order.objects.get(user=current_user, order_number=order_number)
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "shipping": shipping,
                "grand_total": grand_total,
                "payment": response_payment,
            }
            return render(
                request,
                "orders/payments.html",
                context,
            )
    else:
        return redirect("checkout")


def success(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    grand_total = 0
    shipping = 0
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
        grand_total = 0
        shipping = 0

    shipping = (2 * total) / 100
    grand_total = total + shipping
    rz_total = int(grand_total) * 100

    client = razorpay.Client(
        auth=("rzp_test_0DzMFV4V6t3o4d", "qbxeHpoL7mXP5ujLqP8pf4vu"))
    # Create order
    response_payment = client.order.create(dict(amount=rz_total, currency="INR"))

    order_id = response_payment["id"]
    order_status = response_payment["status"]
    if order_status == "created":
        payment = Payment(
            user=request.user,
            amount=rz_total,
            order_id=order_id,
            razorpay_payment_id=response_payment["id"],
            paid=True,
        )

        payment.save()
        response_payment["user"] = current_user

        data = {
            "user ": request.user,
            "order_id": order_id,
            "amount": rz_total,
        }
        # Reduce the quantity of sold items
    for item in cart_items:
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user=current_user).delete()
    return render(request, "orders/success.html", data)
    
    
# View Orders in Admin Panel
def view_order(request):
    orders = Order.objects.all().filter()
    
    context = {
        'orders' : orders,
    }
    return render(request,'admin/view_order.html',context)

# View Payments in Admin Panel
def view_payment(request):
    payments = Payment.objects.all().filter()
    
    context = {
        'payments' : payments,
    }
    return render(request,'admin/view_payment.html',context)

# Cancel Order
def cancel_order(request,pk):
    order = Order.objects.filter(id=pk)
    order.delete()
    messages.success(request,'Product Cancellation processed.')
    return redirect(my_orders)
    