# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render

from firebasedb.models import FirebaseDB

import logging
logger = logging.getLogger(__name__)


class FirebaseDBReachabilityView(View):

    def get(self, request, *args, **kwargs):

        firebase_db = FirebaseDB()
        if firebase_db.get_db_reachability():
            return HttpResponse('Firebase DB is reachable.\n')
        else:
            return HttpResponse('Firebase DB is NOT reachable.\n')


class HttpPutTestView(View):

    def put(self, request, *args, **kwargs):

        logger.info('HttpPutTestView HTTP PUT')
        return HttpResponse('HTTP PUT Handler')