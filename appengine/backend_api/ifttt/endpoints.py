# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseServerError


class IFTTTStatusEndPoint(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse('OK')


class IFTTTBaseEndPoint(View):
    """
    return JSON object
        {
            "data": {
                // The value of `data` varies, but is typically
                // either an object or array
                ...
            }
        }
    """

    def post(self, request, *args, **kwargs):

        # 200: The request was a success.
        resp_data = {
            "data": {}
        }
        return JsonResponse(resp_data)

        err_data = {
            "errors": [
                {
                    "message": "Something went wrong!"
                }
            ]
        }

        # 400: There was something wrong with incoming data from IFTTT.
        # Provide an error response body to clarify what went wrong.
        return JsonResponse(err_data, status=400)

        # 401: IFTTT sent an OAuth2 access token that isn’t valid.
        return JsonResponse(err_data, status=401)

        # 404	IFTTT is trying to reach a URL that doesn’t exist.
        return JsonResponse(err_data, status=404)

        # 500	There was an error in your application logic.
        return JsonResponse(err_data, status=500)

        # 503	Your service is not available at the moment, but IFTTT should try again later.
        return JsonResponse(err_data, status=503)


class IFTTTTestSetupEndPoint(View):

    def post(self, request, *args, **kwargs):

        return HttpResponseServerError('Not Implement Yet')


class IFTTTTestNewThingCreatedTrigger(View):

    def post(self, request, *args, **kwargs):

        return HttpResponseServerError('Not Implement Yet')


class IFTTTStartHC2SceneAction(View):

    def post(self, request, *args, **kwargs):

        return HttpResponseServerError('Not Implement Yet')

