from django.conf.urls import patterns, include, url
from tests.test_app.views import router


urlpatterns = patterns(
    '',
    url(r'^',      include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^owl',   include('owl.urls')),
)
