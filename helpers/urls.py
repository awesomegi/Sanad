from django.urls import path
from . import views
 
app_name = 'helpers'
 
urlpatterns = [
   path('signup/', views.signup_helper, name='signup_helper'),
   path('wait-review/', views.wait_review, name='wait_review'),
   path('signin/', views.signin_helper, name='signin_helper'),
   path('dashboard/', views.helper_dashboard, name='helper_dashboard'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
   path('profile/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
   path('profile/availability/<int:pk>/delete/', views.delete_availability, name='delete_availability'),
   path('bookings/<int:booking_id>/accept/',   views.accept_booking,          name='accept_booking'),
   path('bookings/<int:booking_id>/cancel/',   views.cancel_booking_by_helper, name='cancel_booking_by_helper'),
   path('bookings/<int:booking_id>/complete/', views.complete_booking,         name='complete_booking'),
   path('bookings/<int:booking_id>/rate/',     views.rate_seeker,              name='rate_seeker'),
]