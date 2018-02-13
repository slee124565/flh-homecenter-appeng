# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render

from firebasedb.models import FirebaseDB
import logging
import google.oauth2.id_token

logger = logging.getLogger(__name__)

HTTP_REQUEST = google.auth.transport.requests.Request()


class EchoAPI(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')


class DemoMessagesAPI(View):

    def get(self, request, *args, **kwargs):

        logger.debug('request.META keys: %s' % str(request.META.keys()))
        logger.debug('request.META authorization value %s' % str(request.META.get('HTTP_AUTHORIZATION')))
        id_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()
        logger.debug('DemoMessagesAPI get id_token %s' % id_token)

        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, HTTP_REQUEST)
        if not claims:
            return HttpResponse('Unauthorized', status=401)

        friendly_id = claims.get('name', claims.get('email', 'Unknown'))

        firebase_db = FirebaseDB()
        pi_serial_list = firebase_db.get_dev_serial_list()
        demo_notes = []
        if pi_serial_list:
            for pi_serial in pi_serial_list:
                demo_notes.append({
                    'friendly_id': friendly_id,
                    'message': pi_serial,
                    'created': ''
                })

        response = JsonResponse(demo_notes,safe=False)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        # response["Access-Control-Max-Age"] = "1000"
        # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

        return response