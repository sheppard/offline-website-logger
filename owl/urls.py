from django.conf.urls import patterns, include, url
from .views import LogView


urlpatterns = patterns('',
    url(r'^', LogView.as_view()),
)
