# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

from clients.models import ClientDev

import logging
logger = logging.getLogger(__name__)


class ClientDevTestCase(TestCase):

    def setUp(self):
        self.pi_serial = '000000000635b170'

    def test_get_dev_http_url(self):
        self.client_dev = ClientDev(self.pi_serial)
        self.client_dev.get_dev_http_url()


class ClientDevViewTestCase(TestCase):

    def setUp(self):
        self.pi_serial = '000000000635b170'

    def test_client_dev_view(self):
        test_url = reverse('client_dev_view') + '?pi_serial=' + self.pi_serial
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302, 'client device view open fail.')
        logger.debug('test_client_dev_view with url {view_url}'.format(
            view_url=test_url))
        logger.debug('test_client_dev_view with url {view_url} with response code {code}'.format(
            view_url=reverse('client_dev_view'), code=response.status_code))
