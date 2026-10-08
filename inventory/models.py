from django.db import models

# Create your models here.

# ============================================ CATEGORY Model =================================================
class Category(models.Model):
    
    name =models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name

# ============================================ SUPPLIER Model =================================================
class Supplier(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.name

# ============================================ PRODUCT Model =================================================
class Product(models.Model):
    name  =  models.CharField(max_length=150)
    
    sku = models.CharField(
        max_length=50,
        unique=True
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='Products'
    )
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    quantity = models.PositiveIntegerField(default=0)
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    reoder_level = models.PositiveIntegerField(default=10)
    
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
# ============================================ STOCK TRANSTION =================================================
class StockTransaction(models.Model):
    
    TRANSATION_CHOICE = [
        ('in', 'Stock In'),
        ('out', 'Stock Out')
    ]
    
    product = models.ForeignKey(
        Category,
        on_delete= models.CASCADE,
        related_name='transation'
    )
    
    transaction_type  = models.CharField(  max_length=10, choices=TRANSATION_CHOICE)
    
    quantity = models.PositiveIntegerField()
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )
    
    note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    