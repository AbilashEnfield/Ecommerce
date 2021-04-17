from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='adminLogin'),
    path('admin_signup/', views.admin_signup, name='adminSignup'),
    path('admin_dashboard/', views.admin_dashboard, name='adminPanel'),
    path('new_product/', views.new_product, name='newProduct'),
    path('remove_product/', views.remove_product, name='removeProduct'),
    path('delete_entry/<int:id>', views.delete_entry, name='deleteEntry'),
    path('add_product/', views.add_product, name='addProduct'),
    path('edit_product/<int:id>', views.edit_product, name='editProduct'),
    path('update_product/', views.update_product, name='updateProduct'),
    path('delete_product/', views.delete_product, name='deleteProduct'),
    path('user_database/', views.users_list, name='userDatabase'),
    path('block_user/<int:id>', views.block_user, name='blockUser'),
    path('orders_database/', views.order_list, name='ordersDatabase'),
    path('orders_status/<int:id>/<str:status>', views.order_status, name='ordersStatus'),
    path('discount_list/', views.discount_list, name='discountDatabase'),
    path('discount_delete/<int:id>', views.delete_discount, name='deleteDiscount'),

]
