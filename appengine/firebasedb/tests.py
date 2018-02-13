# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from firebasedb.models import FirebaseDB


class FirebaseDBTestCase(TestCase):

    def setUp(self):
        self.firebase_db = FirebaseDB()
        self.pi_serial = '000000000635b170'

    def test_db_availability(self):
        # firebase_db = FirebaseDB()
        self.assertTrue(self.firebase_db.get_db_reachability(),
                        'firebase database reachability error')

    def test_get_dev_info(self):
        pi_serial = '000000000635b170'
        self.assertNotEqual(self.firebase_db.get_dev_info(self.pi_serial), None,
                            'device({obj.pi_serial}) info not exist.'.format(obj=self))

    def test_get_dev_serial_list(self):
        self.assertNotEqual(self.firebase_db.get_dev_serial_list(), None,
                            'devices serial list not exist.')


class FirebaseDBViewTestCase(TestCase):

    def setUp(self):
        self.pi_serial = '000000000635b170'

    def test_db_reachability_view(self):
        response = self.client.get('/db/reachability/')
        self.assertEqual(response.status_code, 200, 'firebasedb ReachabilityView error.')

    def test_dev_info_view(self):
        response = self.client.get('/db/dev/{pi_serial}/'.format(pi_serial=self.pi_serial))
        self.assertEqual(response.status_code, 200, 'firebasedb device info view error.')

    def test_devs_view(self):
        response = self.client.get('/db/dev/')
        self.assertEqual(response.status_code, 200, 'firebasedb devices view error.')
