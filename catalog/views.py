from django.shortcuts import render
from .models import Brick


def index(request):
    all_bricks = Brick.objects.all()
    return render(request, 'index.html', {'bricks': all_bricks})

