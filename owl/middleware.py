from .models import Session, Event


class ServerEventMiddleware(object):
    def process_response(self, request, response):
        if "html" not in response['Content-type']:
            return response
        session = Session.objects.get_from_request(request)
        Event.objects.create(
            session=session,
            action="server:view",
            path=request.path,
            referer=request.META.get('HTTP_REFERER', None),
            client_date=None,
        )

        return response
