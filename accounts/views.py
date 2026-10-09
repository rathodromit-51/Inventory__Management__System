from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import Profile
from .forms import RegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


# ============================== Register View =============================
def RegisterView(request):
    if request.user.is_authenticate():
        return redirect('')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'staff'
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# ==================================== Login View ====================================
def LoginView(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        ) 
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


# ==================================== Logout View =======================================
@login_required
def LogoutView(request):
    logout(request)
    return redirect('login') 

# ==================================== Dashboard Views ====================================
def manager_dashboard(request):
    return render(request, 'accounts/manager_dashboard.html')


# ==================================== Home ====================================
@login_required
def home(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin')
    elif user.role == 'manager':
        return redirect('manager_dashboard')
    else:
        return render(request, 'dashboard/staff_dashboard.html')