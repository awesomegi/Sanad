from django.urls import path
from . import views
 
app_name = 'helpers'
 
urlpatterns = [
   path('signup/', views.signup_helper, name='signup_helper'),
   path('wait-review/', views.wait_review, name='wait_review'),
   path('signin/', views.signin_helper, name='signin_helper'),
   path('dashboard/', views.helper_dashboard, name='helper_dashboard'), 
   path('profile/edit/', views.edit_profile, name='edit_profile'),
  
]