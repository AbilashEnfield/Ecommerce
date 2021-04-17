from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200, null=True)
    phone_number = models.BigIntegerField(verbose_name="phone number", unique=True)
    image = models.ImageField(null=True, blank=True)
    referralCode = models.CharField(max_length=200, null=True)

    @property
    def userimage(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    # password    = models.CharField(max_length=25, null=True)
    # date_joined = models.DateTimeField(verbose_name='date joined', auto_now=True)
    # last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    #
    # def has_module_perms(self, app_label):
    #     return True


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    miniImage1 = models.ImageField(null=True, blank=True)
    miniImage2 = models.ImageField(null=True, blank=True)
    miniImage3 = models.ImageField(null=True, blank=True)

    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def miniImage1URL(self):
        try:
            url = self.miniImage1.url
        except:
            url = ''
        return url

    @property
    def miniImage2URL(self):
        try:
            url = self.miniImage2.url
        except:
            url = ''
        return url

    @property
    def miniImage3URL(self):
        try:
            url = self.miniImage3.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    CATEGORY_CHOICES = (
        ('Order Placed', "Order Placed"), ('Pending', "Pending"), ('Shipping', "Shipping"), ('Delivered', "Delivered"))
    order_status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    percentage = models.FloatField(default=0, null=True, blank=True)
    StartDate = models.DateTimeField(null=True, blank=True)
    EndDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.percentage)

    @property
    def discountedPrice(self):
        newPrice = self.product.price - (self.product.price * (self.percentage / 100))
        return newPrice


class Coupons(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.CharField(max_length=200, null=True)
    StartDate = models.DateTimeField(null=True, blank=True)
    EndDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.coupon
