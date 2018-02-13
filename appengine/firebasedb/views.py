# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render

from firebasedb.models import FirebaseDB


class ReachabilityView(View):

    def get(self, request, *args, **kwargs):

        firebase_db = FirebaseDB()
        if firebase_db.get_db_reachability():
            return HttpResponse('Firebase DB is reachable.\n')
        else:
            return HttpResponse('Firebase DB is NOT reachable.\n')


class DeviceInfoView(View):

    def get(self, request, *args, **kwargs):

        firebase_db = FirebaseDB()
        pi_serial = self.kwargs.get('pi_serial')
        dev_info = firebase_db.get_dev_info(pi_serial)
        if dev_info:
            return JsonResponse(dev_info)
        else:
            return JsonResponse({})


class DeviceListView(View):

    def get(self, request, *args, **kwargs):

        firebase_db = FirebaseDB()
        dev_serial_list = firebase_db.get_dev_serial_list()
        if dev_serial_list:
            return JsonResponse(dev_serial_list, safe=False)
        else:
            return JsonResponse([], safe=False)
