from django.contrib import admin
from .models import Client, Session, Event


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'browser', 'user_agent']
    list_filter = ['ip_address']
    inlines = [SessionInline]


class SessionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'client']
    list_filter = ['user', 'client__ip_address']


class EventAdmin(admin.ModelAdmin):
    list_display = ['session', 'action', 'path', 'server_date', 'lag']
    list_filter = ['action', 'server_date', 'session']


admin.site.register(Client, ClientAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Event, EventAdmin)
