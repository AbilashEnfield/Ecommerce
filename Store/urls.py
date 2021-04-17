from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('delete_item/<int:id>', views.deleteItem, name='delete_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('product_details/<int:id>', views.product_Details, name='product_details'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='editProfile'),
    path('order_placed/', views.order_Placed, name='orderPlaced'),
    path('apply_coupon/<str:total>', views.apply_coupon, name='applyCoupon'),

]
