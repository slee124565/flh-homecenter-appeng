# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError

from .models import ClientHC2
import logging
logger = logging.getLogger(__name__)


class BaseJsonResponse(JsonResponse):

    def __init__(self, err_code=0, err_msg='Success'):
        super(BaseJsonResponse, self).__init__(
            {
                'code': err_code,
                'msg': err_msg
            }
        )


class ExceptionJsonResponse(BaseJsonResponse):

    ERR_CODE = 0xff

    def __init__(self, exc_msg):

        super(ExceptionJsonResponse, self).__init__(self.ERR_CODE, exc_msg)


class FlhHc2EchoAPI(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')


class FlhHc2SceneControlAPI(View):

    def get(self, request, *args, **kwargs):
        try:
            logger.debug('FlhHc2SceneControlAPI GET API')
            scene_name = request.GET.get('s', '')
            room_name = request.GET.get('r', None)
            lang_code = request.GET.get('c', None)
            client_key = request.GET.get('k', None)
            logger.debug('%s GET API trigger with %s, %s, %s, %s' % (
                self.__class__.__name__, scene_name, room_name, lang_code, client_key))

            # query client by client_key
            client_hc2 = ClientHC2.get_client_by_key(client_key)
            if client_hc2 is None:
                return BaseJsonResponse(1, 'client not exist')

            # trigger client scene api
            if client_hc2.control_hc2_scene(scene_name, room_name, lang_code):
                return BaseJsonResponse(0, 'scene [%s] in room [%s] start cmd sent' % (scene_name, room_name))
            else:
                return BaseJsonResponse(2, 'client cmd sent error')
        except Exception as e:
            logger.warning('%s HTTP GET Exception' % self.__class__.__name__, exc_info=True)
            return ExceptionJsonResponse(e.message)

    @classmethod
    def api_test(cls):
        import requests
        payload = {
            's': 'environmental information',
            'c': 'en',
            'k': 'showroom'
        }
        url = 'https://freqoserv-dot-solar-cloud-143410.appspot.com/s/h/i/sc'
        r = requests.get(url, params=payload)
        logger.info('{cls.__name__} api_test status code {r.status_code}\n {r.content}'.format(cls=cls, r=r))
