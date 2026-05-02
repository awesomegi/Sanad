from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('checkout/<int:booking_id>/pay/', views.fake_pay, name='fake_pay'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('failed/<int:booking_id>/', views.payment_failed, name='payment_failed'),
]