from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Brick, Order
from .cart import Cart
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages


def create_order_view(request, brick_id):
    if request.method == 'POST':
        brick = get_object_or_404(Brick, id=brick_id)

        # Получаем данные из полей формы
        quantity = request.POST.get('quantity')
        mixture_weight = request.POST.get('mixture_weight', 0)
        client_name = request.POST.get('client_name')
        client_phone = request.POST.get('client_phone')

        # Создаем запись в базе данных
        Order.objects.create(
            brick=brick,
            quantity=quantity,
            mixture_weight=mixture_weight,
            client_name=client_name,
            client_phone=client_phone
        )

        # После успешного заказа перенаправляем на страницу «Спасибо за заказ»
        # Или можно просто вернуть на главную
        return render(request, 'order_success.html', {'client_name': client_name})

    return redirect('brick_detail', brick_id=brick_id)

def index(request):
    if request.method == 'POST':
        brick_id = request.POST.get('brick_id')
        user_name = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')
        brick = Brick.objects.get(id=brick_id)
        Order.objects.create(brick=brick, name=user_name, phone=user_phone)
        return redirect('index')

    all_bricks = Brick.objects.all()
    return render(request, 'index.html', {'bricks': all_bricks})

# Страница отдельного товара с калькулятором
def brick_detail(request, brick_id):
    # Находим кирпич по ID или показываем ошибку 404, если такого нет
    brick = get_object_or_404(Brick, id=brick_id)
    return render(request, 'brick_detail.html', {'brick': brick})


def search_view(request):
    query = request.GET.get('q', '').strip()

    if query:
        # Ищем совпадения по имени без учета регистра
        matched_bricks = [b for b in Brick.objects.all() if query.lower() in b.name.lower()]

        # Если нашли ровно один товар (например, ввели "шб-5"), сразу перекидываем на его страницу
        if len(matched_bricks) == 1:
            return redirect('brick_detail', brick_id=matched_bricks[0].id)

        results = matched_bricks
    else:
        results = Brick.objects.all()

    return render(request, 'search_results.html', {'results': results, 'query': query})


def brick_description_views(request, brick_id):
    brick = get_object_or_404(Brick, id=brick_id)
    return render(request, 'brick_description.html', {'brick': brick})


@require_POST
def cart_add(request, brick_id):
    """Добавление товара в корзину"""
    cart = Cart(request)
    brick = get_object_or_404(Brick, id=brick_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(brick=brick, quantity=quantity)
    return redirect('cart_detail')


def cart_remove(request, brick_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    brick = get_object_or_404(Brick, id=brick_id)
    cart.remove(brick)
    return redirect('cart_detail')


def cart_detail(request):
    """Страница отображения корзины"""
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


@require_POST
def cart_checkout(request):
    cart = Cart(request)
    client_name = request.POST.get('client_name')
    client_phone = request.POST.get('client_phone')

    # Здесь в будущем можно сохранять заказ в базу данных (модель Order)
    # или отправлять уведомление в Telegram/Email.

    # Очищаем корзину после успешного оформления
    cart.clear()

    # Перенаправляем на вашу готовую красивую страницу «Спасибо за заказ»
    return render(request, 'order_success.html', {'client_name': client_name})


def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = authenticate(request, username=u_name, password=p_word)
        if user is not None:
            auth_login(request, user)
            return redirect('index') # перенаправляем на главную
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        if User.objects.filter(username=u_name).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            User.objects.create_user(username=u_name, password=p_word)
            return redirect('login') # после регистрации отправляем на вход
    return render(request, 'register.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index')







