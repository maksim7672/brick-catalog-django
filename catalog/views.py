from django.shortcuts import render, redirect, get_object_or_404
from .models import Brick, Order


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