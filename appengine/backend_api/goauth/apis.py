# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

import urllib
import json
import google.oauth2.id_token
import datetime

import logging
logger = logging.getLogger(__name__)


# Structure of Auth
# {
#     'clients': {
#     '< client id >': {
#         'clientSecret': '< value >',
#         'uid': '< value >'
#         }
#     },
#     'tokens': {
#     '< token id >': {
#         '< uid >': {}
#         },
#     },
#     'users': {
#     '< uid >': {
#         'name': '< username >',
#         'password': '< password >',
#         'tokens': [ '< token id >', ],
#         'clients': [ '< client id >', ]
#         }
#     }
# }


class AuthStore(object):

    clients = {
        'dfb1e2a9cd55889cd778fd7aad8406d0': {}
    }
    auth_codes = {
        '908c65cf20628acd45f8e63ce6bbc796': {
            'type': 'AUTH_CODE',
            'uid': 'up5GqFgKb4OMoInRlIIqTTL3i9W2',
            'client_id': 'dfb1e2a9cd55889cd778fd7aad8406d0',
            'expires_at': datetime.datetime.now() + datetime.timedelta(seconds=(60 * 10000))
        }
    }
    tokens = {
        'psokmCxKjfhk7qHLeYd1': {
          'uid': 'up5GqFgKb4OMoInRlIIqTTL3i9W2',
          'accessToken': 'psokmCxKjfhk7qHLeYd1',
          'refreshToken': 'psokmCxKjfhk7qHLeYd1',
          'userId': '1234'
        },
    }

    @classmethod
    def generate_auth_code(cls, uid, client_id):
        devp_auth_code = '908c65cf20628acd45f8e63ce6bbc796'
        auth_code = devp_auth_code

        return auth_code

    @staticmethod
    def get_client(client_id, client_secret):
        return {
            'client_id': client_id,
            'client_secret': client_secret
        }

    @classmethod
    def get_auth_code(cls, code):
        auth_code = cls.auth_codes.get(code, None)
        devp_expires_at = datetime.datetime.now() + datetime.timedelta(seconds=(60 * 10000))
        auth_code['expires_at'] = devp_expires_at
        return auth_code

    @classmethod
    def check_uid(cls, uid):
        return True

    @classmethod
    def get_token_by_uid(cls, uid):
        return {
            'uid': '1234',
            'access_token': 'psokmCxKjfhk7qHLeYd1',
            'refresh_token': 'psokmCxKjfhk7qHLeYd1',
        }

    @classmethod
    def get_access_token(cls, code):
        dev_access_token = {
            'token_type': 'bearer',
            'access_token': 'psokmCxKjfhk7qHLeYd1',
            'refresh_token': 'psokmCxKjfhk7qHLeYd1'
        }
        return dev_access_token

        # let authCode = authstore.authcodes[code];
        # if (!authCode) {
        # console.error('invalid code');
        # return false;
        # }
        auth_code = AuthStore.get_auth_code(code)
        if auth_code is None:
            logger.error('invalid code')
            return None

        # if (new Date(authCode.expiresAt) < Date.now()) {
        # console.error('expired code');
        # return false;
        # }
        #
        if auth_code.get('expires_at') < datetime.datetime.now():
            logger.error('expired code')
            return None

        # let user = authstore.users[authCode.uid];
        # if (!user) {
        # console.error('could not find user');
        # return false;
        # }
        if not AuthStore.check_uid(auth_code.get('uid')):
            logger.error('could not find user')
            return None

        # let accessToken = authstore.tokens[user.tokens[0]];
        # console.log('getAccessToken = ', accessToken);
        # if (!accessToken || !accessToken.uid) {
        # console.error('could not find accessToken');
        # return false;
        # }
        #
        uid_token = AuthStore.get_token_by_uid(auth_code.get('uid'))
        if uid_token is None:
            logger.error('could not find accessToken')
            return None

        # let returnToken = {
        # token_type: "bearer",
        # access_token: accessToken.accessToken,
        # refresh_token: accessToken.refreshToken
        # };
        #
        access_token = {
            'token_type': 'bearer',
            'access_token': uid_token.get('access_token'),
            'refresh_token': uid_token.get('refresh_token')
        }

        # console.log('return getAccessToken = ', returnToken);
        # return returnToken;
        logger.debug('return token %s' % str(access_token))
        return access_token


class OAuthLogin(View):

    def post(self, request, *args, **kwargs):
        pass


class OAuthAPI(View):

    @staticmethod
    def oauth_handler(request):

        if request.method == 'GET':
            client_id = request.GET.get('client_id', None)
            redirect_uri = request.GET.get('redirect_uri', None)
            state = request.GET.get('state', None)
            response_type = request.GET.get('response_type', None)
            auth_code = request.GET.get('auth_code', None)
            id_token = request.GET.get('id_token', None)
        else:
            client_id = request.POST.get('client_id', None)
            redirect_uri = request.POST.get('redirect_uri', None)
            state = request.POST.get('state', None)
            response_type = request.POST.get('response_type', None)
            auth_code = request.POST.get('auth_code', None)
            id_token = request.GET.get('id_token', None)

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
            'response_type': response_type,
            'auth_code': auth_code,
            'id_token': id_token
        }
        logger.info('oauth api params:\n%s' % json.dumps(params, indent=2))

        if response_type != 'code':
            return HttpResponseServerError('response_type {response_type} must equal "code"'.format(
                response_type=response_type))

        if AuthStore.clients.get(client_id, None) is None:
            return HttpResponseServerError('client_id {client_id} invalid'.format(
                client_id=client_id
            ))

        # // if you have an authcode use that
        if auth_code:
            return HttpResponseRedirect('%s?code=%s&state=%s' % (redirect_uri, auth_code, state))

        # // Redirect anonymous users to login page.
        if id_token:
            HTTP_REQUEST = google.auth.transport.requests.Request()
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, HTTP_REQUEST)
        else:
            claims = None

        if not claims:
            query_string = urllib.urlencode(params)
            logger.info('redirect login with query string %s' % query_string)
            return HttpResponseRedirect('/#!/login?%s' % query_string)
        else:
            user_id = claims.get('user_id')
            friendly_id = claims.get('name', claims.get('email', 'Unknown'))
            logger.info('%s login successful user_id %s' % (friendly_id, user_id))

        # Redirect to user to original app server
        auth_code = AuthStore.generate_auth_code(user_id, client_id)
        params['auth_code'] = auth_code
        if auth_code:
            if redirect_uri:
                logger.debug('authCode successful %s' % auth_code)
                return HttpResponseRedirect('%s?code=%s&state=%s' % (
                    redirect_uri, auth_code, state
                ))
            else:
                return HttpResponse(json.dumps(params, indent=2))

        return HttpResponseBadRequest('something went wrong')

    def get(self, request, *args, **kwargs):
        return OAuthAPI.oauth_handler(request)

    def post(self, request, *args, **kwargs):
        return OAuthAPI.oauth_handler(request)


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
            code = request.GET.get('code', None)
        else:
            client_id = request.POST.get('client_id', None)
            client_secret = request.POST.get('client_secret', None)
            code = request.POST.get('code', None)

        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        }
        logger.info('handle_auth_code params\n%s' % json.dumps(params, indent=2))

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
        logger.info('respond success %s' % str(token))
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

        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        }
        logger.info('handle_refresh_token params\n%s' % json.dumps(params, indent=2))

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

        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type
        }
        logger.info('token_exchange_handler params:\n%s' % json.dumps(params, indent=2))

        logger.info('(client_id is None) %s' % str((client_id is None)))
        logger.info('(client_secret is None) %s' % str((client_secret is None)))
        if (client_id is None) or (client_secret is None):
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
