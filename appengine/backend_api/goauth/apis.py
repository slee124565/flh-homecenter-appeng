# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.urls import reverse

import urllib
import google.oauth2.id_token

import logging
logger = logging.getLogger(__name__)


class AuthStore(object):
    clients = {
        'dfb1e2a9cd55889cd778fd7aad8406d0': {}
    }


class OAuthAPI(View):

    def get(self, request, *args, **kwargs):

        client_id = request.GET.get('client_id', None)
        redirect_uri = request.GET.get('redirect_uri', None)
        state = request.GET.get('state', None)
        response_type = request.GET.get('response_type', None)
        auth_code = request.GET.get('code', None)

        if response_type != 'code':
            return  HttpResponseServerError('response_type ' + response_type + ' must equal "code"')

        if AuthStore.clients.get(client_id, None) is None:
            return HttpResponseServerError('client_id ' + client_id + ' invalid')

        # // if you have an authcode use that
        if auth_code:
            return HttpResponseRedirect('%s?code=%s&state=%s' % (redirect_uri, auth_code, state))
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ').pop()
        logger.debug('get auth_token %s' % auth_token)

        HTTP_REQUEST = google.auth.transport.requests.Request()
        claims = google.oauth2.id_token.verify_firebase_token(
            auth_token, HTTP_REQUEST)

        # // Redirect anonymous users to login page.
        # if (!user)
        # {
        #     return res.redirect(util.format('/login?client_id=%s&redirect_uri=%s&redirect=%s&state=%s',
        #                                 client_id, encodeURIComponent(redirect_uri), req.path, state));
        # }
        if not claims:
            return HttpResponseRedirect('/login?client_id=%s&redirect_uri=%s&redirect=%s&state=%s' % (
                client_id, urllib.urlencode(redirect_uri), reverse('oauth_code_api'), state
            ))

        # console.log('login successful ', user.name);
        friendly_id = claims.get('name', claims.get('email', 'Unknown'))
        logger.info('login successful %s' % friendly_id)

        # authCode = SmartHomeModel.generateAuthCode(user.uid, client_id);
        #
        # if (authCode) {
        #     console.log('authCode successful ', authCode);
        #     return res.redirect(util.format('%s?code=%s&state=%s',
        #     redirect_uri, authCode, state));
        # }

        return HttpResponseBadRequest('something went wrong')


class TokenExAPI(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')
