from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
import datetime
import random

# Create your views here.


def store(request):
    code = random.randint(10000, 99999)
    couponCode = f"XMAS{code}"
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if Coupons.objects.filter(customer=customer).exists():
            user_coupon = Coupons.objects.filter(customer=customer).first()
            couponCode = user_coupon.coupon
        else:
            code = random.randint(10000, 99999)
            couponCode = f"XMAS{code}"
            Coupons.objects.create(customer=customer, coupon=couponCode)

        discounts = Discount.objects.all()
        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems, 'discounts': discounts, 'couponCode': couponCode}
        return render(request, 'store/store.html', context)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        discounts = Discount.objects.all()
        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems, 'discounts': discounts, 'couponCode': couponCode}
        return render(request, 'store/store.html', context)

    # discounts = Discount.objects.all()
    # products = Product.objects.all()
    # context = {'products': products, 'cartItems': cartItems, 'discounts': discounts, 'couponCode': couponCode}
    # return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    discounts = Discount.objects.all()
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'discounts': discounts}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if Coupons.objects.filter(customer=customer).exists():
            user_coupon = Coupons.objects.filter(customer=customer).first()
            couponCode = user_coupon.coupon
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    discounts = Discount.objects.all()
    newTotal = order.get_cart_total
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'discounts': discounts, 'newTotal': newTotal, 'couponCode': couponCode}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def deleteItem(request, id):
    if id is not None:
        item = OrderItem.objects.get(id=id)
        print(item)
        item.delete()
    return redirect('cart')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
    return JsonResponse('Payment completed!', safe=False)


def product_Details(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'store/productDetails.html', context)


def user_profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.filter(customer=customer)
    items = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        items.append(order_items)

    context = {'customer': customer, 'items': items}
    return render(request, 'store/userProfile.html', context)


def edit_profile(request):
    if request.method == "POST":

        return redirect('user_profile')
    else:
        user = request.user
        customer = Customer.objects.get(user=user)

        context = {'customer': customer}
        return render(request, 'store/editProfile.html', context)


def order_Placed(request):
    return redirect('store')


def apply_coupon(request, total):
    newTotal = 0
    initialTotal = float(total)

    if request.user.is_authenticated:
        customer = request.user.customer
        if Coupons.objects.filter(customer=customer).exists():
            user_coupon = Coupons.objects.filter(customer=customer).first()
            if user_coupon.coupon is not None:
                newTotal = (initialTotal * 0.5)
                user_coupon.delete()
            else:
                newTotal = initialTotal

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    discounts = Discount.objects.all()
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'discounts': discounts, 'newTotal': newTotal}
    return render(request, 'store/checkout.html', context)
