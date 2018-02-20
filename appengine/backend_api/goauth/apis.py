# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse


class OAuthAPI(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')


class TokenExAPI(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')
