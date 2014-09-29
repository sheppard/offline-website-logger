from rest_framework.serializers import ModelSerializer
from rest_framework.fields import DateTimeField
from .models import Client, Event
from datetime import datetime
from django.utils.timezone import utc


class EpochField(DateTimeField):
    def from_native(self, value):
        if value is not None:
            date = datetime.utcfromtimestamp(float(value))
            date = date.replace(tzinfo=utc)
            return date


class EventSerializer(ModelSerializer):
    client_date = EpochField(required=False)

    def from_native(self, data, files):
        client = Client.objects.get_from_request(
            self.context['request']
        )
        data['client'] = client.pk
        return super(EventSerializer, self).from_native(data, files)

    class Meta:
        model = Event
