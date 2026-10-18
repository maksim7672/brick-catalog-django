from django.db import models

from django.db import models


class Brick(models.Model):
    name = models.CharField(max_length=50)        # Название (например, ШБ-5)
    size = models.CharField(max_length=30)        # Размеры (например, 230х114х65 мм)
    price = models.IntegerField()                 # Цена (просто целое число)
    description = models.TextField()
    image = models.ImageField(upload_to='bricks_photos/', blank=True, null=True)
    mixture_per_brick = models.FloatField(default=0.4, verbose_name="Расход смеси на 1 шт (кг)")

    def __str__(self):
        return self.name  # Чтобы в админке красиво писалось имя кирпича, а не "Brick object"


class Order(models.Model):
    brick = models.ForeignKey(Brick, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество (шт)")
    mixture_weight = models.FloatField(verbose_name="Смесь (кг)")
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    client_phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} — {self.client_name} ({self.brick.name})"