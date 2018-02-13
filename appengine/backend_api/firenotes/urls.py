
from django.conf.urls import url

from .apis import DemoMessagesAPI
from .apis import EchoAPI

urlpatterns = [

    # == backend api for admin start ==
    url(r'^notes$', DemoMessagesAPI.as_view()),

    url(r'^echo', EchoAPI.as_view()),
]

