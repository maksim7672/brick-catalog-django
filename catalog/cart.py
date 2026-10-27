from decimal import Decimal
from django.conf import settings
from .models import Brick


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, brick, quantity=1, override_quantity=False):
        brick_id = str(brick.id)
        if brick_id not in self.cart:
            self.cart[brick_id] = {'quantity': 0, 'price': str(brick.price)}

        if override_quantity:
            self.cart[brick_id]['quantity'] = quantity
        else:
            self.cart[brick_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, brick):
        brick_id = str(brick.id)
        if brick_id in self.cart:
            del self.cart[brick_id]
            self.save()

    def __iter__(self):
        brick_ids = self.cart.keys()
        bricks = Brick.objects.filter(id__in=brick_ids)
        cart = self.cart.copy()

        for brick in bricks:
            cart[str(brick.id)]['brick'] = brick

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()