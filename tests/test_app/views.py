from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from .models import Item


class ItemViewSet(ModelViewSet):
    model = Item

router = DefaultRouter()
router.register('items', ItemViewSet, 'item')
