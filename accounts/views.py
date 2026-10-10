from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import Profile
from .forms import RegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


# ============================== Register View =============================
def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'staff'
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please check your inputs and try again.')
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
    messages.info(request, 'You have been successfully logged out.')
    return redirect('login') 

from inventory.models import Product, Category, Supplier, StockTransaction
from accounts.decorators import role_required
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count

# ==================================== Dashboard Views ====================================
@role_required(['manager', 'admin'])
def manager_dashboard(request):
    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    suppliers_count = Supplier.objects.count()
    transactions_count = StockTransaction.objects.count()

    low_stock_qs = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).select_related('category', 'supplier')
    low_stock_count = low_stock_qs.count()

    valuation_expr = ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField())
    total_valuation = Product.objects.annotate(val=valuation_expr).aggregate(total=Sum('val'))['total'] or 0

    recent_transactions = StockTransaction.objects.select_related('product', 'user').order_by('-created_at')[:8]
    categories_summary = Category.objects.annotate(prod_count=Count('Products'))[:6]
    suppliers_summary = Supplier.objects.annotate(prod_count=Count('products'))[:6]
    recent_products = Product.objects.select_related('category', 'supplier').order_by('-created_at')[:6]

    context = {
        'products_count': products_count,
        'categories_count': categories_count,
        'suppliers_count': suppliers_count,
        'transactions_count': transactions_count,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_qs[:5],
        'total_valuation': total_valuation,
        'recent_transactions': recent_transactions,
        'categories_summary': categories_summary,
        'suppliers_summary': suppliers_summary,
        'recent_products': recent_products,
    }
    return render(request, 'dashboard/manager_dashboard.html', context)


@role_required(['admin'])
def admin_dashboard(request):
    users_count = Profile.objects.count()
    staff_count = Profile.objects.filter(role='staff').count()
    manager_count = Profile.objects.filter(role='manager').count()
    admin_count = Profile.objects.filter(role='admin').count()
    recent_users = Profile.objects.order_by('-date_joined')[:6]

    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    suppliers_count = Supplier.objects.count()
    transactions_count = StockTransaction.objects.count()

    valuation_expr = ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField())
    total_valuation = Product.objects.annotate(val=valuation_expr).aggregate(total=Sum('val'))['total'] or 0

    low_stock_qs = Product.objects.filter(quantity__lte=F('reorder_level'))
    low_stock_count = low_stock_qs.count()
    recent_transactions = StockTransaction.objects.select_related('product', 'user').order_by('-created_at')[:10]

    context = {
        'users_count': users_count,
        'staff_count': staff_count,
        'manager_count': manager_count,
        'admin_count': admin_count,
        'recent_users': recent_users,
        'products_count': products_count,
        'categories_count': categories_count,
        'suppliers_count': suppliers_count,
        'transactions_count': transactions_count,
        'total_valuation': total_valuation,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ==================================== Home Role Dispatcher ====================================
@login_required
def home(request):
    user = request.user
    if user.is_superuser or getattr(user, 'role', '') == 'admin':
        return redirect('admin_dashboard')
    elif getattr(user, 'role', '') == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('staff_dashboard')