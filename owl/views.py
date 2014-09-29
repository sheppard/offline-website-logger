from rest_framework_bulk import BulkCreateAPIView
from rest_framework.renderers import JSONRenderer

from .models import Event
from .serializers import EventSerializer


class LogView(BulkCreateAPIView):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    renderer_classes = [JSONRenderer]

    def dispatch(self, request, *args, **kwargs):
        response = super(LogView, self).dispatch(request, *args, **kwargs)
        response.data = {}
        return response
