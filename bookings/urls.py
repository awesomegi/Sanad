from django.urls import path
from . import views
 
app_name = 'bookings'
 
urlpatterns = [
    path('',            views.helpers_list,  name='helpers_list'),
    path('<int:pk>/detail/', views.helper_detail, name='helper_detail'),
    path('rate/<int:booking_id>/', views.rate_helper, name='rate_helper'),
]