from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, StockTransaction, Supplier
from .forms import SupplierForm, ProductForm, CategoryForm, StockTransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import update_stock
from accounts.decorators import role_required
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

# ============================================ DASHBOARD =================================================
@login_required
def staff_dashboard(request):
    categories_count = Category.objects.count()
    products_count = Product.objects.count()
    suppliers_count = Supplier.objects.count()
    transactions_count = StockTransaction.objects.count()
    
    # Query low stock items
    low_stock_qs = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).select_related('category', 'supplier')
    low_stock_count = low_stock_qs.count()
    
    # Total Inventory Valuation
    valuation_expr = ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField())
    total_valuation = Product.objects.annotate(val=valuation_expr).aggregate(total=Sum('val'))['total'] or 0
    
    # Recent Transactions & Products
    recent_transactions = StockTransaction.objects.select_related('product', 'user').order_by('-created_at')[:6]
    recent_products = Product.objects.select_related('category').order_by('-created_at')[:5]
    
    context = {
        'categories_count': categories_count,
        'products_count': products_count,
        'suppliers_count': suppliers_count,
        'transactions_count': transactions_count,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_qs[:5],
        'total_valuation': total_valuation,
        'recent_transactions': recent_transactions,
        'recent_products': recent_products,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

# ============================================ CATEGORY =================================================

# ADD CATEGORY
@role_required(['staff', 'manager', 'admin'])
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Failed to create category. Please check the form errors.')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form, 'title': 'Add New Category'})

# VIEW CATEGORY
@login_required
def category_view(request):
    categories = Category.objects.all().prefetch_related('Products')
    return render(request, 'inventory/category_list.html', {'categories': categories})

# UPDATE CATEGORY
@role_required(['manager', 'admin'])
def update_category_view(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Failed to update category. Please check form errors.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form, 'category': category, 'title': f'Edit Category: {category.name}'})

# DELETE CATEGORY
@role_required(['admin'])
def delete_category_view(request, id):
    category = get_object_or_404(Category, id=id)
    name = category.name
    category.delete()
    messages.success(request, f'Category "{name}" deleted successfully!')
    return redirect('category_list')


# ============================================ PRODUCT =================================================

# ADD PRODUCT
@role_required(['staff', 'manager', 'admin'])
def add_product_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added to inventory!')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to create product. Please verify all fields.')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add New Product'})

# VIEW PRODUCTS
@login_required
def product_detail_view(request):
    products = Product.objects.select_related('category', 'supplier').all()
    categories = Category.objects.all()
    return render(request, 'inventory/products_list.html', {
        'products': products,
        'categories': categories,
    })

# VIEW SINGLE PRODUCT
@login_required
def single_product_view(request, id):
    product = get_object_or_404(Product.objects.select_related('category', 'supplier'), id=id)
    recent_transactions = product.transactions.select_related('user').order_by('-created_at')[:10]
    return render(request, 'inventory/product_detail.html', {
        'product': product,
        'recent_transactions': recent_transactions
    })

# UPDATE PRODUCT
@role_required(['manager', 'admin'])
def update_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to update product.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'product': product, 'title': f'Edit Product: {product.name}'})

# DELETE PRODUCT
@role_required(['admin'])
def delete_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" removed from inventory!')
    return redirect('product_list')


# ============================================ SUPPLIER =================================================

# ADD SUPPLIER
@role_required(['staff', 'manager', 'admin'])
def add_supplier_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" added successfully!')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Failed to add supplier.')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form, 'title': 'Add New Supplier'})

# VIEW SUPPLIER
@login_required
def supplier_view(request):
    suppliers = Supplier.objects.all().prefetch_related('products')
    return render(request, 'inventory/supplier_list.html', {'supplier': suppliers})

# UPDATE SUPPLIER
@role_required(['manager', 'admin'])
def update_supplier_view(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f'Supplier "{supplier.name}" updated successfully!')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Failed to update supplier.')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form, 'supplier': supplier, 'title': f'Edit Supplier: {supplier.name}'})

# DELETE SUPPLIER
@role_required(['admin'])
def delete_supplier_view(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    name = supplier.name
    supplier.delete()
    messages.success(request, f'Supplier "{name}" deleted successfully!')
    return redirect('supplier_list')


# ============================================ STOCK =================================================

# ADD STOCK TRANSACTION
@login_required
def add_stock_transaction_view(request):
    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            t_type = form.cleaned_data['transaction_type']
            qty = form.cleaned_data['quantity']
            note = form.cleaned_data.get('note', '')
            try:
                update_stock(p_id=product.id, s_quantity=qty, transaction_type=t_type)
                if note:
                    last_txn = StockTransaction.objects.filter(product=product).order_by('-id').first()
                    if last_txn:
                        last_txn.user = request.user
                        last_txn.note = note
                        last_txn.save(update_fields=['user', 'note'])
                messages.success(request, f'Stock {t_type.upper()} of {qty} units for "{product.name}" completed!')
                return redirect('stock_list')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the transaction form.')
    else:
        form = StockTransactionForm(initial={'user': request.user})
    return render(request, 'inventory/stock_transaction_form.html', {'form': form, 'title': 'Record Stock Movement'})

# VIEW STOCK
@login_required
def stock_transaction_view(request):
    stock_transactions = StockTransaction.objects.select_related('product', 'user').order_by('-created_at')
    return render(request, 'inventory/stock_list.html', {'stock_transactions': stock_transactions})

# DELETE STOCK
@role_required(['admin'])
def delete_stock_transaction_view(request, id):
    stock_transaction = get_object_or_404(StockTransaction, id=id)
    stock_transaction.delete()
    messages.success(request, 'Stock transaction record removed.')
    return redirect('stock_list')

# ADJUST STOCK
@login_required
def adjust_stock_view(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 0))
        stock_type = request.POST.get("transaction_type")
        note = request.POST.get("note", "")

        try:
            update_stock(
                p_id=id,
                s_quantity=quantity,
                transaction_type=stock_type  
            )
            if note:
                last_txn = StockTransaction.objects.filter(product=product).order_by('-id').first()
                if last_txn:
                    last_txn.user = request.user
                    last_txn.note = note
                    last_txn.save(update_fields=['user', 'note'])
            messages.success(request, f'Stock for "{product.name}" successfully updated ({stock_type.upper()} {quantity})')
            return redirect('product_list')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'inventory/stock_transaction_form.html', { "product": product, 'title': f'Quick Stock Adjustment: {product.name}' })


def home_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    total_transactions = StockTransaction.objects.count()
    return render(request, 'inventory/home.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'total_transactions': total_transactions,
    })