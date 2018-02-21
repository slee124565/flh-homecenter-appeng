# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

import urllib
import google.oauth2.id_token
import datetime

import logging
logger = logging.getLogger(__name__)


class AuthStore(object):
    clients = {
        'dfb1e2a9cd55889cd778fd7aad8406d0': {}
    }
    auth_codes = {}

    @classmethod
    def generate_auth_code(cls, uid, client_id):
        import hashlib
        m = hashlib.md5()
        m.update(uid + client_id)
        auth_code = m.hexdigest()

        cls.auth_codes[auth_code] = {
            'type': 'AUTH_CODE',
            'uid': uid,
            'client_id': client_id,
            'expires_at': datetime.datetime.now() + datetime.timedelta(seconds=(60 * 10000))
        };

        return auth_code

    @staticmethod
    def get_client(client_id, client_secret):
        return {
            'client_id': client_id,
            'client_secret': client_secret
        }

    @classmethod
    def get_auth_code(cls, code):
        return cls.auth_codes.get(code, None)

    @classmethod
    def get_access_token(cls, code):
        """
        # let authCode = authstore.authcodes[code];
        # if (!authCode) {
        # console.error('invalid code');
        # return false;
        # }
        # if (new Date(authCode.expiresAt) < Date.now()) {
        # console.error('expired code');
        # return false;
        # }
        #
        # let user = authstore.users[authCode.uid];
        # if (!user) {
        # console.error('could not find user');
        # return false;
        # }
        # let accessToken = authstore.tokens[user.tokens[0]];
        # console.log('getAccessToken = ', accessToken);
        # if (!accessToken || !accessToken.uid) {
        # console.error('could not find accessToken');
        # return false;
        # }
        #
        # let returnToken = {
        # token_type: "bearer",
        # access_token: accessToken.accessToken,
        # refresh_token: accessToken.refreshToken
        # };
        #
        # console.log('return getAccessToken = ', returnToken);
        # return returnToken;
        """


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
        if not claims:
            return HttpResponseRedirect('/login?client_id=%s&redirect_uri=%s&redirect=%s&state=%s' % (
                client_id, urllib.urlencode(redirect_uri), reverse('oauth_code_api'), state
            ))

        # console.log('login successful ', user.name);
        user_id = claims.get('user_id')
        friendly_id = claims.get('name', claims.get('email', 'Unknown'))
        logger.info('%s login successful user_id %s' % (friendly_id, user_id))

        # Redirect to user to original app server
        auth_code = AuthStore.generate_auth_code(user_id, client_id)
        if auth_code:
            logger.debug('authCode successful %s' % auth_code)
            return HttpResponseRedirect('%s?code=%s&state=%s' % (
                redirect_uri, auth_code, state
            ))

        return HttpResponseBadRequest('something went wrong')


class TokenExAPI(View):

    @staticmethod
    def handle_auth_code(request):
        # console.log('handleAuthCode', req.query);
        # let client_id = req.query.client_id ? req.query.client_id : req.body.client_id;
        # let client_secret = req.query.client_secret ? req.query.client_secret : req.body.client_secret;
        # let code = req.query.code ? req.query.code : req.body.code;
        if request.method == 'GET':
            client_id = request.GET.get('client_id', None)
            client_secret = request.GET.get('client_secret', None)
            code = request.GET.get('refresh_token', None)
        else:
            client_id = request.POST.get('client_id', None)
            client_secret = request.POST.get('client_secret', None)
            code = request.POST.get('refresh_token', None)

        #
        # if (!code) {
        # console.error('missing required parameter');
        # return res.status(400).send('missing required parameter');
        # }
        if code is None:
            logger.error('missing required parameter')
            return HttpResponseBadRequest('missing required parameter')

        #
        # let client = SmartHomeModel.getClient(client_id, client_secret);
        # if (!client) {
        # console.error('invalid client id or secret %s, %s', client_id, client_secret);
        # return res.status(400).send('invalid client id or secret');
        # }
        oauth_client = AuthStore.get_client(client_id, client_secret)
        if oauth_client is None:
            logger.error('invalid client id or secret %s, %s' % (client_id, client_secret))
            return HttpResponseBadRequest('invalid client id or secret')

        #
        # let authCode = authstore.authcodes[code];
        # if (!authCode) {
        # console.error('invalid code');
        # return res.status(400).send('invalid code');
        # }
        auth_code = AuthStore.get_auth_code(code)
        if auth_code is None:
            logger.error('invalid code')
            return HttpResponseBadRequest('invalid code')

        # if (new Date(authCode.expiresAt) < Date.now()) {
        # console.error('expired code');
        # return res.status(400).send('expired code');
        # }
        if auth_code.get('expires_at') < datetime.datetime.now():
            logger.error('expired code')
            return HttpResponseBadRequest('expired code')

        # if (authCode.clientId != client_id) {
        # console.error('invalid code - wrong client', authCode);
        # return res.status(400).send('invalid code - wrong client');
        # }
        if auth_code.get('client_id') != client_id:
            logger.error('invalid code - wrong client' + auth_code)
            return HttpResponseBadRequest('invalid code - wrong client')

        #
        # let token = SmartHomeModel.getAccessToken(code);
        # if (!token) {
        # console.error('unable to generate a token', token);
        # return res.status(400).send('unable to generate a token');
        # }
        token = AuthStore.get_access_token(code)
        if token is None:
            logger.error('unable to generate a token %s' % str(token))
            return HttpResponseBadRequest('unable to generate a token')
        #
        # console.log('respond success', token);
        # return res.status(200).json(token);
        logger.info('respond success ' + token)
        return JsonResponse(token)

    @staticmethod
    def handle_refresh_token(request):
        if request.method == 'GET':
            client_id = request.GET.get('client_id', None)
            client_secret = request.GET.get('client_secret', None)
            refresh_token = request.GET.get('refresh_token', None)
        else:
            client_id = request.POST.get('client_id', None)
            client_secret = request.POST.get('client_secret', None)
            refresh_token = request.POST.get('refresh_token', None)

        oauth_client = AuthStore.get_client(client_id, client_secret)
        if oauth_client is None:
            logger.error('invalid client id or secret %s, %s' % (client_id, client_secret))
            return HttpResponseServerError('invalid client id or secret')

        if refresh_token is None:
            logger.error('missing required parameter')
            return HttpResponseServerError('missing required parameter')

        return JsonResponse(
            {
                'token_type': 'bearer',
                'access_token': refresh_token
            }
        )

    def token_exchange_handler(self, request):
        if request.method == 'GET':
            client_id = request.GET.get('client_id', None)
            client_secret = request.GET.get('client_secret', None)
            grant_type = request.GET.get('grant_type', None)
        else:
            client_id = request.POST.get('client_id', None)
            client_secret = request.POST.get('client_secret', None)
            grant_type = request.POST.get('grant_type', None)

        if client_id is None or client_secret is None:
            logger.error('missing required parameter')
            return HttpResponseBadRequest('missing required parameter')

        oauth_client = AuthStore.get_client(client_id, client_secret)
        logger.debug('client %s' % str(oauth_client))

        if oauth_client is None:
            logger.error('incorrect client data')
            return HttpResponseBadRequest('incorrect client data')

        if grant_type == 'authorization_code':
            return self.handle_auth_code(request)
        elif grant_type == 'refresh_token':
            return self.handle_refresh_token(request)
        else:
            logger.error('grant_type ' + grant_type + ' is not supported')
            return HttpResponseBadRequest('grant_type ' + grant_type + ' is not supported')

    def get(self, request, *args, **kwargs):
        return self.token_exchange_handler(request)

    def post(self,request, *args, **kwargs):
        return self.token_exchange_handler(request)
