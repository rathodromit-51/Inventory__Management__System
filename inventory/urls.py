from django.urls import path
from .views import *

urlpatterns = [
    path('category/add/', add_category_view, name='add_category'),
    path('category/list/', category_view, name='category_list'),
    path('category/update/<int:id>/', update_category_view, name='update_category'),
    path('category/delete/<int:id>/', delete_category_view, name='delete_category'),
    
    path('product/add/', add_product_view, name='add_product'),
    path('product/list/', product_detail_view, name='product_list'),
    path('product/<int:id>/', single_product_view, name='product_detail'),
    path('product/update/<int:id>/', update_product_view, name='update_product'),
    path('product/delete/<int:id>/', delete_product_view, name='delete_product'),
    
    path('supplier/add/', add_supplier_view, name='add_supplier'),
    path('supplier/list/', supplier_view, name='supplier_list'),
    path('supplier/update/<int:id>/', update_supplier_view, name='update_supplier'),
    path('supplier/delete/<int:id>/', delete_supplier_view, name='delete_supplier'),
    
    path('stock/add/', add_stock_transaction_view, name='add_stock'),
    path('stock/list/', stock_transaction_view, name='stock_list'),
    path('stock/update/<int:id>/', adjust_stock_view, name='update_stock'),
    path('stock/delete/<int:id>/', delete_stock_transaction_view, name='delete_stock'),
    
    path('dashboard/', staff_dashboard, name='dashboard'),
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('', home_view, name='home'),
]