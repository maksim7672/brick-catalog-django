from django.shortcuts import render, redirect
from .models import Brick, Order  # Импортируем и Кирпич, и Заказ


def index(request):
    # Если пользователь нажал кнопку отправки формы (купить)
    if request.method == 'POST':
        brick_id = request.POST.get('brick_id')
        user_name = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')

        # Находим кирпич, который хочет купить клиент
        brick = Brick.objects.get(id=brick_id)

        # Создаем новый заказ в базе данных
        Order.objects.create(brick=brick, name=user_name, phone=user_phone)

        # Перезагружаем страницу, чтобы форма очистилась и не дублировалась
        return redirect('index')

    # Это обычный показ кирпичей при заходе на сайт
    all_bricks = Brick.objects.all()
    return render(request, 'index.html', {'bricks': all_bricks})