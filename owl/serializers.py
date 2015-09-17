from rest_framework.serializers import ModelSerializer
from rest_framework.fields import DateTimeField
from .models import Session, Event
from datetime import datetime
from django.utils.timezone import utc


class EpochField(DateTimeField):
    def to_internal_value(self, value):
        if value is not None:
            date = datetime.utcfromtimestamp(float(value))
            date = date.replace(tzinfo=utc)
            return date


class EventSerializer(ModelSerializer):
    client_date = EpochField(required=False)

    def to_internal_value(self, data):
        session = Session.objects.get_from_request(
            self.context['request']
        )
        data['session'] = session.pk
        return super(EventSerializer, self).to_internal_value(data)

    class Meta:
        model = Event
