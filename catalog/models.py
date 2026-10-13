from django.db import models

from django.db import models


class Brick(models.Model):
    name = models.CharField(max_length=50)        # Название (например, ШБ-5)
    size = models.CharField(max_length=30)        # Размеры (например, 230х114х65 мм)
    price = models.IntegerField()                 # Цена (просто целое число)
    description = models.TextField()
    image = models.ImageField(upload_to='bricks_photos/', blank=True, null=True)

    def __str__(self):
        return self.name  # Чтобы в админке красиво писалось имя кирпича, а не "Brick object"
