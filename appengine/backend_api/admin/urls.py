
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import FirebaseDBReachabilityView
from .views import HttpPutTestView

urlpatterns = [

    # == backend api for admin start ==
    url(r'^views/db_reachability/$', FirebaseDBReachabilityView.as_view(), name='db_reachability_view'),

    url(r'^views/test_http_put/$', csrf_exempt(HttpPutTestView.as_view())),

]

