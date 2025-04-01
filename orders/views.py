# from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse
# from carts.models import CartItem
# from .forms import OrderForm
# import datetime
# from .models import Order, Payment, OrderProduct
# import json
# from store.models import Product
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string

# # Create your views here.

# def payments(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
#     # Store transaction details inside payment model
#     payment = Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = order.order_total,
#         status = body['status'],
#     )
#     payment.save()

#     order.payment = payment
#     order.is_ordered = True
#     order.save()

#     #move the card item to order product table
#     cart_items = CartItem.objects.filter(user=request.user)
#     for items in cart_items:
#         orderproduct = OrderProduct()
#         orderproduct.order_id = order.id
#         orderproduct.payment = payment
#         orderproduct.user_id = request.user.id
#         orderproduct.product_id = items.product_id
#         orderproduct.quantity = items.quantity
#         # orderproduct.variations = item.variations
#         orderproduct.product_price = items.product.price
#         orderproduct.ordered = True
#         orderproduct.save()

#         orderproduct.variations.set(items.variations.all())

#             # cart_item = CartItem.objects.get(id=item.id)
#             # product_variation = cart_item.variations.all()
#             # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#             # orderproduct.variations.set(product_variation)
#             # orderproduct.save()
            
#         #reduce the quantity of the sold products
#         product = Product.objects.get(id=items.product_id)
#         product.stock -= items.quantity
#         product.save()
    
#     #clear the card after the order Is completed :)
#     CartItem.objects.filter(user=request.user).delete()


#     #send email after order is completed
#     mail_subject = 'Your Order is completed Successfully, Thankyou for your ordering form us!'
#     message = render_to_string('orders/order_recieved_email.html', {
#         'user' : request.user,
#         'order' : order,
#     })
#     to_email = request.user.email
#     send_email = EmailMessage(mail_subject, message, to=[to_email])
#     send_email.send()
    

#     #send transaction details to order complete page
#     data = {
#         'order_number' : order.order_number,
#         'transID' : payment.payment_id,

#     }
#     return JsonResponse(data)

# def place_order(request, total=0, quantity=0):
    
#     current_user = request.user

#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')
    
#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (0.2 * total)/100
#     grand_total = total + tax
    
    

#     if request.method == 'POST':
#         form = OrderForm(request.POST) 
#         if form.is_valid():
#             #store all the billing information inside order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.pin = form.cleaned_data['pin']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             #generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime("%Y%m%d")
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()

#             order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

#             context = {
#                 'order' : order,
#                 'cart_items' : cart_items,
#                 'total' : total,
#                 'tax' : tax,
#                 'grand_total' : grand_total,
#         }
            
#         return render(request, 'orders/payments.html', context)
#     else:

#      return redirect('checkout')
    

# # def order_complete(request):
# #     order_number = request.GET.get('order_number')
# #     transID = request.GET.get('payment_id')
    
# #     try:
# #         order = Order.objects.get(order_number=order_number, is_ordered=True)
# #         ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
# #         payment = Payment.objects.get(payment_id=transID)

# #         context = {
# #             'order' : order,
# #             'ordered_products' : ordered_products,
# #             'order_number' : order.order_number,
# #             'transID' : payment.payment_id,
# #             'payment' : payment,
# #         }
# #         return render(request, 'orders/order_complete.html', context)
# #     except(Payment.DoesNotExist, Order.DoesNotExist):
# #         return redirect('home')
    
# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     payment_id = request.GET.get('payment_id')

#     try:
#         order = Order.objects.get(order_number=order_number)
#         payment = Payment.objects.get(payment_id=payment_id)
#         ordered_products = OrderProduct.objects.filter(order=order)

#         subtotal = 0 
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         context = {
#             'order': order,
#             'payment': payment,
#             'ordered_products': ordered_products,
#             'order_number': order_number,
#             'transID': payment.payment_id,
#             'subtotal': subtotal,
#         }
#         return render(request, 'orders/order_complete.html', context)

#     except (Order.DoesNotExist, Payment.DoesNotExist):
#         return redirect('home')  # Redirects to home if order/payment not found   

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    # Store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    #move the card item to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for items in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = items.product_id
        orderproduct.quantity = items.quantity
        # orderproduct.variations = item.variations
        orderproduct.product_price = items.product.price
        orderproduct.ordered = True
        orderproduct.save()

        orderproduct.variations.set(items.variations.all())

            # cart_item = CartItem.objects.get(id=item.id)
            # product_variation = cart_item.variations.all()
            # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            # orderproduct.variations.set(product_variation)
            # orderproduct.save()
            
        #reduce the quantity of the sold products
        product = Product.objects.get(id=items.product_id)
        product.stock -= items.quantity
        product.save()
    
    #clear the card after the order Is completed :)
    CartItem.objects.filter(user=request.user).delete()


    #send email after order is completed
    mail_subject = 'Your Order is completed Successfully, Thankyou for your ordering form us!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user' : request.user,
        'order' : order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    

    #send transaction details to order complete page
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,

    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (0.2 * total)/100
    grand_total = total + tax
    
    

    if request.method == 'POST':
        form = OrderForm(request.POST) 
        if form.is_valid():
            #store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin = form.cleaned_data['pin']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
        }
            
        return render(request, 'orders/payments.html', context)
    else:

     return redirect('checkout')
    

# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')
    
#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order' : order,
#             'ordered_products' : ordered_products,
#             'order_number' : order.order_number,
#             'transID' : payment.payment_id,
#             'payment' : payment,
#         }
#         return render(request, 'orders/order_complete.html', context)
#     except(Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')
    
def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number)
        payment = Payment.objects.get(payment_id=payment_id)
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal = 0 
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'payment': payment,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')  # Redirects to home if order/payment not found   