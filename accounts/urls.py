from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('manager-dashboard/', manager_dashboard, name='manager_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('home/', home, name='home')
]