from django.urls import path
from . import views

#added by rimas
app_name = 'payments'

urlpatterns = [
    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('checkout/<int:booking_id>/pay/', views.fake_pay, name='fake_pay'),
    path('callback/', views.moyasar_callback, name='moyasar_callback'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('failed/<int:booking_id>/', views.payment_failed, name='payment_failed'),
    path('refund/<int:booking_id>/confirm/', views.refund_confirm, name='refund_confirm'),
    path('refund/<int:booking_id>/process/', views.process_refund, name='process_refund'),  
    path('refund/<int:booking_id>/success/', views.refund_success, name='refund_success'),  
]