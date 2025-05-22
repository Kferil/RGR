from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Product, CartItem, Order, OrderItem
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.shortcuts import render

# Главная
def index(request):
    return render(request, 'notes/index.html')

# Каталог
def catalog(request):
    category = request.GET.get('category')
    if category == 'women':
        products = Product.objects.filter(category='women')
    elif category == 'men':
        products = Product.objects.filter(category='men')
    else:
        products = Product.objects.all()
    return render(request, 'notes/catalog.html', {'products': products})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите.')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    return render(request, 'notes/register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})

# Выход
@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')

# Личный кабинет
@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('items__product')
    return render(request, 'notes/profile.html', {
        'user': user,
        'orders': orders
    })

# Добавление в корзину
def add_to_cart(request, product_id):
    if not request.session.session_key:
        request.session.create()
        request.session.save()

    session_key = request.session.session_key
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
            session_key=session_key
        )
    else:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            session_key=session_key,
            user=None
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

# Просмотр корзины
@login_required
def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    return render(request, 'notes/cart.html', {'cart_items': cart_items})

# Оформление заказа
@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST' and cart_items.exists():
        order = Order.objects.create(user=request.user, is_completed=True)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()  # очищаем корзину
        return render(request, 'checkout_success.html', {'order': order})

    return render(request, 'notes/checkout.html', {'cart_items': cart_items})

# Просмотр заказов
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'notes/orders.html', {'orders': orders})

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        item = get_object_or_404(CartItem, id=item_id, session_key=session_key)
        item.delete()
    return redirect('cart')

def checkout_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    if request.method == 'POST':
        if not cart_items.exists():
            return redirect('catalog')

        # Создаём заказ
        order = Order.objects.create(user=request.user if request.user.is_authenticated else None)

        # Копируем товары из корзины в заказ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Очищаем корзину
        cart_items.delete()

        return redirect('checkout_success')

    return render(request, 'notes/checkout.html', {'cart_items': cart_items})

def checkout_success_view(request):
    return render(request, 'notes/checkout_success.html')



