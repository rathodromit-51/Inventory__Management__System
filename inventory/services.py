from django.db import transaction
from .models import Product, StockTransaction

@transaction.atomic
def update_stock(p_id, s_quantity, transaction_type):

    if s_quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    
    product = Product.objects.get(id=p_id)
    
    if transaction_type == 'in':
        product.quantity += s_quantity
    
    elif transaction_type == 'out':
        if product.quantity >= s_quantity:
            product.quantity -= s_quantity
        else:
            raise ValueError('Insufficient stock')
    else:
        raise ValueError('Invalid transaction type')
    
    product.save(update_fields=['quantity'])
    
    StockTransaction.objects.create(
        product=product,
        transaction_type=transaction_type,
        quantity=s_quantity
    )
    
    return product