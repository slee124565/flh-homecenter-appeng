
from django.conf.urls import url

from .apis import OAuthAPI
from .apis import TokenExAPI

urlpatterns = [

    # == backend api for admin start ==
    url(r'^oauth', OAuthAPI.as_view(), name='oauth_code_api'),

    url(r'^token', TokenExAPI.as_view(), name='oauth_token_api'),
]
