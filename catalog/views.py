from django.shortcuts import redirect, get_object_or_404
from .models import Product, CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Здесь должна быть логика добавления в корзину (например, по user или сессии)
    cart_item = CartItem.objects.create(product=product, quantity=1)
    return redirect('catalog')  # имя страницы, на которую возвращаться
