from django import forms
from .models import Category, Product, Supplier, StockTransaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'email',
            'phone'
        ]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'sku',
            'category',
            'supplier',
            'quantity',
            'price',
            'reorder_level',
            'description'
        ]
        
class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = [
            'product', 
            'transition_type', 
            'quantity', 
            'user', 
            'note'
        ]