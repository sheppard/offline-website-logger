from django.conf.urls import patterns, url
from .views import LogView


urlpatterns = patterns(
    '',
    url(r'^', LogView.as_view()),
)
