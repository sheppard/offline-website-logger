from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer
from .models import Item


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

router = DefaultRouter()
router.register('items', ItemViewSet, 'item')
