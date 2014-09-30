from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
import swapper
from django.core.urlresolvers import resolve, Resolver404


class ClientManager(models.Manager):
    def get_from_request(self, request):
        user = request.user
        if not user.is_authenticated():
            user = None
        ip_address = request.META.get('REMOTE_ADDR', None)
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        if isinstance(request.DATA, list) and len(request.DATA) > 0:
            client_key = request.DATA[0].get('key', None)
        else:
            client_key = None
        server_key = request.session._get_or_create_session_key()
        client, is_new = self.get_or_create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            client_key=client_key,
            server_key=server_key,
        )
        return client


class Client(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(null=True, blank=True, max_length=255)
    client_key = models.CharField(null=True, blank=True, max_length=255)
    server_key = models.CharField(null=True, blank=True, max_length=255)
    user = models.ForeignKey(
        swapper.get_model_name('auth', 'User'), null=True, blank=True
    )

    objects = ClientManager()

    def __str__(self):
        if self.user is not None:
            return str(self.user)
        return self.ip_address

    class Meta:
        unique_together = ['ip_address', 'user_agent', 'user']


class Event(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    client_date = models.DateTimeField(null=True, blank=True)
    server_date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    referer = models.URLField(null=True, blank=True)
    action = models.CharField(max_length=20, default="view")
    data = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def lag(self):
        if self.client_date:
            return self.server_date - self.client_date

    def save(self, **kwargs):
        if self.path and not self.object_id:
            self.resolve_path()
        return super(Event, self).save(**kwargs)

    def resolve_path(self):
        """
        Attempt to resolve a URL path into a class instance
        """
        try:
            resolved = resolve(self.path)
        except Resolver404:
            return

        func = resolved.func
        if not hasattr(func, 'cls'):
            return

        if not (hasattr(func.cls, 'model') or hasattr(func.cls, 'queryset')):
            return

        cls = getattr(func.cls, 'model', None)
        if not cls:
            cls = func.cls.queryset.model

        try:
            instance = cls.objects.get(**resolved.kwargs)
        except cls.DoesNotExist:
            return

        self.content_object = instance

    def __str__(self):
        return "%s %sed %s" % (self.client, self.action, self.path)
