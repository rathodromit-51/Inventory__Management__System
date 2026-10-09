from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('manager-dashboard/', manager_dashboard, name='manager_dashboard'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
    path('home/', home, name='home')
]