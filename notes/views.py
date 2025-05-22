from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Product, CartItem
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect

def index(request):
    return render(request, 'notes/index.html')

def catalog(request):
    # Получаем параметр фильтрации из URL, например ?category=women
    category = request.GET.get('category')

    if category == 'women':
        products = Product.objects.filter(category='women')
    elif category == 'men':
        products = Product.objects.filter(category='men')
    else:
        products = Product.objects.all()

    return render(request, 'notes/catalog.html', {'products': products})

def add_to_cart(request, product_id):
    if not request.session.session_key:
        request.session.create()  # создаём сессию, если её ещё нет

    product = get_object_or_404(Product, id=product_id)

    # Пытаемся найти уже существующий товар в корзине
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=request.session.session_key
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    return render(request, 'notes/cart.html', {'cart_items': cart_items})






# ... остальные функции ...



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаем пользователя
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите.')
            return redirect('login')
        else:
            # Если форма невалидна — покажем ошибки
            errors = form.errors.as_json()
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print(errors)  # Для отладки в консоли сервера
    else:
        form = RegisterForm()
    return render(request, 'notes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # после входа в личный кабинет
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})


@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    # Можно передать в шаблон ещё данные, например заказы пользователя
    return render(request, 'notes/profile.html', {'user': user})

