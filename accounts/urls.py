from django.urls import path
from . import views

urlpatterns = [
    path('signup/seeker/', views.signup_seeker, name='signup_seeker'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),  # ← add this

]