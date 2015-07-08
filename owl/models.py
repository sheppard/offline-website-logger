from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
import swapper
from django.core.urlresolvers import resolve, Resolver404


class ClientManager(models.Manager):
    def get_from_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR', None)
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        client, is_new = self.get_or_create(
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return client


class Client(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(null=True, blank=True, max_length=255)
    objects = ClientManager()

    def __str__(self):
        return self.ip_address

    @property
    def browser(self):
        if not self.user_agent:
            return None
        from ua_parser import user_agent_parser
        result = user_agent_parser.Parse(self.user_agent)
        return result['user_agent']['family']

    class Meta:
        unique_together = [
            'ip_address', 'user_agent',
        ]


class SessionManager(models.Manager):
    def get_from_request(self, request):
        client = Client.objects.get_from_request(request)
        user = None
        if hasattr(request, 'user') and request.user.is_authenticated():
            user = request.user

        DATA = getattr(request, 'DATA', None)
        if isinstance(DATA, list) and len(DATA) > 0:
            client_key = request.DATA[0].get('client_key', None)
        else:
            client_key = None

        if hasattr(request, "session"):
            server_key = request.session._session_key
        else:
            server_key = None
        session, is_new = self.get_or_create(
            user=user,
            client=client,
            client_key=client_key,
            server_key=server_key,
        )
        return session


class Session(models.Model):
    client = models.ForeignKey(Client)
    client_key = models.CharField(null=True, blank=True, max_length=255)
    server_key = models.CharField(null=True, blank=True, max_length=255)
    user = models.ForeignKey(
        swapper.get_model_name('auth', 'User'), null=True, blank=True
    )

    objects = SessionManager()

    def __str__(self):
        if self.user is not None:
            user = str(self.user)
        else:
            user = self.client.ip_address
        return "%s/%s@%s" % (
            user,
            self.client.browser,
            self.client_key[:5] if self.client_key else "server"
        )

    class Meta:
        unique_together = [
            'client', 'user', 'client_key', 'server_key'
        ]


class Event(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True)
    client_date = models.DateTimeField(null=True, blank=True)
    server_date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    referer = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=255, default="view")
    data = models.TextField(null=True, blank=True)

    @property
    def lag(self):
        if self.client_date:
            delta = self.server_date - self.client_date
            if delta.days < 0:
                # Negative delta - client clock is fast or server is slow
                delta = -delta
                return "-%s" % (
                    (delta.seconds * 1e6 + delta.microseconds) / 1e6
                )
            return delta

    def __str__(self):
        return "%s %sed %s" % (self.session, self.action, self.path)

    class Meta:
        ordering = ["-server_date"]
