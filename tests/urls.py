from django.conf.urls import patterns, include, url
from tests.test_app.views import router


urlpatterns = patterns('',
    url(r'^',       include(router.urls)),
    url(r'^owl',    include('owl.urls')),
)
