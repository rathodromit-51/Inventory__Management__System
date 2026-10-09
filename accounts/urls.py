from django.urls import path
from .views import RegisterView, LoginView, LogoutView 


urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
]