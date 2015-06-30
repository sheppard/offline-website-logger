from .models import Session, Event
import json


class ServerEventMiddleware(object):
    def process_response(self, request, response):
        if "html" not in response['Content-type']:
            return response
        session = Session.objects.get_from_request(request)
        referer = request.META.get('HTTP_REFERER', None)
        if request.method == 'GET':
            action = 'view'
        else:
            action = request.method.lower()
        path = request.get_full_path()
        data = self.get_event_data(request)
        if len(path) > 255:
            data['path'] = path
            path = path[:255]

        if response.status_code != 200:
            data['status'] = response.status_code

        Event.objects.create(
            session=session,
            action="server:%s" % action,
            path=path,
            referer=referer,
            client_date=None,
            data=json.dumps(data),
        )

        return response

    def get_event_data(self, request):
        return {}
