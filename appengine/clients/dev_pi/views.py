# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponsePermanentRedirect, HttpResponseBadRequest

from clients.models import ClientDev

import logging
logger = logging.getLogger(__name__)


class DevicePiView(View):

    def get(self, request, *args, **kwargs):
        pi_serial = request.GET.get('pi_serial')
        client_dev = ClientDev(pi_serial)
        client_http_tunnel = client_dev.get_dev_http_url()
        if client_http_tunnel:
            return HttpResponsePermanentRedirect(client_http_tunnel)
        else:
            return HttpResponseBadRequest('client device not reachable.')

    # def post(self, request, *args, **kwargs):
    #     try:
            # logger.debug('request body: %s' % request.body)
            # post_config = json.loads(request.body.decode('utf-8'))
            # logger.debug('SiteWifiConfigApiView post with %s' % str(post_config))
            # if post_config.get('ssid') and post_config.get('psk'):
            #     pi = Smirror(logger=logger)
            #     pi.config_wifi_wpa(post_config.get('ssid'),
            #                         post_config.get('psk'))
            #     wifi_config = pi.get_wifi_config()
            #     return JsonResponse(wifi_config)
            #     #return HttpResponse('OK')
            # else:
            #     logger.warning('Post Param Error: ssid %s, psk %s' % (post_config.get('ssid'),
            #                                                           post_config.get('psk')))
            #     return HttpResponseBadRequest('Post Param Error\n')
        # except:
            # logger.warning('SiteWifiConfigApiView Exception', exc_info=True)
            # return HttpResponseServerError('Server Internal Error')
