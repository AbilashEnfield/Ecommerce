from django.urls import path
from .import views


urlpatterns = [

    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signout/', views.user_signout, name='userSignout'),
    # path('admin_login/', views.admin_login, name='admin_login'),
    path('otp/', views.otp_generate, name='otp_gen'),
    path('otp_validate/', views.otp_validate, name='otp_val'),
    path('send_referral/', views.send_referral, name='sendReferral'),
    path('user_referral_signup/<str:referral>', views.referral_signup, name='userefup'),
]
