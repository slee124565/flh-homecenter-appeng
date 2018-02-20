
from django.conf.urls import url

from .apis import OAuthAPI
from .apis import TokenExAPI

urlpatterns = [

    # == backend api for admin start ==
    url(r'^oauth', OAuthAPI.as_view()),

    url(r'^token', TokenExAPI.as_view()),
]
