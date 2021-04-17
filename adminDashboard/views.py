from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Store.models import Product, Customer, Order, OrderItem, Discount
import base64
from django.core.files.base import ContentFile


# Create your views here.
def admin_login(request):
    return render(request, 'adminDashboard/adminLogin.html')


def admin_signup(request):
    return render(request, 'adminDashboard/adminSignup.html')


def admin_dashboard(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    Jan = Order.objects.filter(date_ordered__year='2021', date_ordered__month='01', ).count()
    Feb = Order.objects.filter(date_ordered__year='2021', date_ordered__month='02', ).count()
    Mar = Order.objects.filter(date_ordered__year='2021', date_ordered__month='03', ).count()
    Apr = Order.objects.filter(date_ordered__year='2021', date_ordered__month='04', ).count()

    context = {'customer': customer, 'Jan': Jan, 'Feb': Feb, 'Mar': Mar, 'Apr': Apr}
    return render(request, 'adminDashboard/adminDashboard.html', context)


def new_product(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    products = Product.objects.all()
    print(products)
    context = {'products': products, 'customer': customer}
    return render(request, 'adminDashboard/newproduct.html', context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        cost = request.POST.get('price')
        if request.POST.get('digital') == 'yes':
            digital = True
        else:
            digital = False
        mainImage = request.POST.get('mainImage')
        miniImage1 = request.POST.get('mainImage1')
        miniImage2 = request.POST.get('mainImage2')
        miniImage3 = request.POST.get('mainImage3')

        format, img = mainImage.split(';base64,')
        ext = format.split('/')[-1]
        img_data = ContentFile(base64.b64decode(img), name=name + '.' + ext)

        format, img1 = miniImage1.split(';base64,')
        ext = format.split('/')[-1]
        img_data1 = ContentFile(base64.b64decode(img1), name=name + '1.' + ext)

        format, img2 = miniImage2.split(';base64,')
        ext = format.split('/')[-1]
        img_data2 = ContentFile(base64.b64decode(img2), name=name + '2.' + ext)

        format, img3 = miniImage3.split(';base64,')
        ext = format.split('/')[-1]
        img_data3 = ContentFile(base64.b64decode(img3), name=name + '3.' + ext)

        Product.objects.create(name=name, price=cost, image=img_data, miniImage1=img_data1, miniImage2=img_data2,
                               miniImage3=img_data3, digital=digital)
        return redirect('addProduct')

    user = request.user
    customer = Customer.objects.get(user=user)
    context = {'customer': customer}
    return render(request, 'adminDashboard/addProduct.html', context)


def edit_product(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    product = Product.objects.get(id=id)
    context = {'product': product, 'customer': customer}
    return render(request, 'adminDashboard/editProduct.html', context)


def update_product(request):
    if request.method == "POST":
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        name = request.POST.get('product_name')
        if name != "":
            product.name = name
        cost = request.POST.get('price')
        if cost != "":
            product.price = cost
        digital = request.POST.get('digital')
        if digital != "":
            if request.POST.get('digital') == 'yes':
                digital = True
            else:
                digital = False
            product.digital = digital
        mainImage = request.POST.get('mainImage')
        print('hi')
        print(mainImage)
        miniImage1 = request.POST.get('mainImage1')
        miniImage2 = request.POST.get('mainImage2')
        miniImage3 = request.POST.get('mainImage3')
        if mainImage != "":
            format, img = mainImage.split(';base64,')
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(img), name=name + '.' + ext)
            product.image = img_data
        if miniImage1 != "":
            format, img1 = miniImage1.split(';base64,')
            ext = format.split('/')[-1]
            img_data1 = ContentFile(base64.b64decode(img1), name=name + '1.' + ext)
            product.miniImage1 = img_data1
        if miniImage2 != "":
            format, img2 = miniImage2.split(';base64,')
            ext = format.split('/')[-1]
            img_data2 = ContentFile(base64.b64decode(img2), name=name + '2.' + ext)
            product.miniImage2 = img_data2
        if miniImage3 != "":
            format, img3 = miniImage3.split(';base64,')
            ext = format.split('/')[-1]
            img_data3 = ContentFile(base64.b64decode(img3), name=name + '3.' + ext)
            product.miniImage3 = img_data3

        product.save()
        return redirect('newProduct')


def delete_product(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context = {'customer': customer}
    return render(request, 'adminDashboard/deleteProduct.html', context)


def remove_product(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    products = Product.objects.all()
    context = {'products': products, 'customer': customer}
    return render(request, 'adminDashboard/removeProduct.html', context)


def delete_entry(request, id):
    Product.objects.filter(id=id).delete()
    return redirect('removeProduct')


def users_list(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    users = Customer.objects.all()
    for x in users:
        print(x.user.is_active)
    context = {'customer': customer, 'users': users}
    return render(request, 'adminDashboard/userDatabase.html', context)


def block_user(request, id):
    print(id)
    user = Customer.objects.get(id=id)
    print(user)
    if user.user.is_active == True:
        user.user.is_active = False
    else:
        user.user.is_active = True
    user.user.save()
    return redirect('userDatabase')


def order_list(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.all
    context = {'orders': orders, 'customer': customer}
    return render(request, 'adminDashboard/orderDatabase.html', context)


def order_status(request, id, status):
    order = Order.objects.get(id=id)

    if status == "Pending":
        order.order_status = 'Pending'
    elif status == "Ordered":
        order.order_status = 'Order Placed'
    elif status == "Shipping":
        order.order_status = 'Shipping'
    elif status == "Delivered":
        order.order_status = 'Delivered'
    order.save()
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.all
    context = {'orders': orders, 'customer': customer}
    return render(request, 'adminDashboard/orderDatabase.html', context)


def discount_list(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        productWithObject = Product.objects.get(name=product)
        percentage = request.POST.get('discount')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        Discount.objects.create(product=productWithObject, percentage=percentage, StartDate=startDate, EndDate=endDate)
        return redirect('discountDatabase')

    else:
        user = request.user
        customer = Customer.objects.get(user=user)
        discounts = Discount.objects.all()
        products = Product.objects.all()
        context = {'discounts': discounts, 'customer': customer, 'products': products}
        return render(request, 'adminDashboard/discountDatabase.html', context)


def add_discount(request):
    return redirect('discountDatabase')


def delete_discount(request, id):
    Discount.objects.filter(id=id).delete()
    return redirect('discountDatabase')
