from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, StockTransaction, Supplier
from .forms import SupplierForm, ProductForm, CategoryForm, StockTransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import update_stock
from accounts.decorators import role_required
from django.db.models import F

def staff_dashboard(request):
    categories = Category.objects.count()
    products = Product.objects.count()
    suppliers = Supplier.objects.count()
    
    low_stock_products = Product.objects.filter(
        quantity__lt = F('reorder_level')
    ).count()
    
    context = {
        'categories' : categories,
        'products' : products,
        'low_stock_products': low_stock_products,
        'suppliers' : suppliers,
    }
    return render(request, 'inventory/dashboard.html', context)

# *******************************  Category ****************************

# ADD CATEGORY
@role_required(['manager', 'admin'])
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form})

# VIEW CATEGORY
@role_required(['manager', 'admin'])
def category_view(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

# UPDATE CATEGORY
@role_required(['manager', 'admin'])
def update_category_view(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form})

# DELETE CATEGORY
@role_required(['admin'])
def delete_category_view(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')


# *******************************  PRODUCT ****************************

# ADD PRODUCT
@role_required(['manager', 'admin'])
def add_product_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

# VIEW PRODUCT
@role_required(['manager', 'admin'])
def product_detail_view(request):
    products = Product.objects.all()
    return render(request, 'inventory/products_list.html', {'products': products})

# vIEW SINGLE PRODUCT
@role_required(['manager', 'admin'])
def single_product_view(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'inventory/single_product.html', {'product': product})

# UPDATE PRODUCT
@role_required(['manager', 'admin'])
def update_product_view(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

# DELETE PRODUCT
@role_required(['admin'])
def delete_product_view(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products_list')


# ******************************* SUPPLIER ****************************

# ADD SUPPLIER
@role_required(['manager', 'admin'])
def add_supplier_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form})

# VIEW SUPPLIER
@role_required(['manager', 'admin'])
def supplier_view(request):
    supplier = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'supplier': supplier})

# UPDATE SUPPLIER
@role_required(['manager', 'admin'])
def update_supplier_view(request, id):
    supplier = Supplier.objects.get(id=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form})

# DELETE SUPPLIER
@role_required(['admin'])
def delete_supplier_view(request, id):
    supplier = Supplier.objects.get(id=id)
    supplier.delete()
    return redirect('supplier_list')


# ******************************* STOCK ****************************

# ADD STOCK
@login_required
def add_stock_transaction_view(request):
    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockTransactionForm()
    return render(request, 'inventory/stock_transaction_form.html', {'form': form})

# VIEW STOCK
@login_required
def stock_transaction_view(request):
    stock_transactions = StockTransaction.objects.all()
    return render(request, 'inventory/stock_list.html', {'stock_transactions': stock_transactions})

# DELETE STOCK
@role_required(['admin'])
def delete_stock_transaction_view(request, id):
    stock_transaction = StockTransaction.objects.get(id=id)
    stock_transaction.delete()
    return redirect('stock_list')


# UPDATE STOCK
@role_required(['manager', 'admin'])
def adjust_stock_view(request, p_id):
    product = get_object_or_404(Product, id=p_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 0))
        stock_type = request.POST.get("transaction_type")

        try:
            update_stock(
                p_id= p_id,
                s_quantity= quantity,
                transaction_type = stock_type  
            )
            messages.success(request, 'Stock updated successfully')
            return redirect('product_list')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'inventory/stock_transaction_form.html', { "product": product })
        


