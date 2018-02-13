# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.db import models

import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

from django.conf import settings

import logging
logger = logging.getLogger(__name__)


class FirebaseDB(object):

    _default_app = None

    def __init__(self, db_name='default'):
        if FirebaseDB._default_app is None:
            if settings.FIREBASE_DBS.get(db_name, None):
                logger.debug('firebase db init with {config}'.format(
                    config=settings.FIREBASE_DBS.get(db_name)))
                FirebaseDB._default_app = firebase_admin.initialize_app(
                    credentials.Certificate(settings.FIREBASE_DBS.get(db_name)['cert_file']), {
                        'databaseURL': settings.FIREBASE_DBS.get(db_name)['db_url_root']
                    })
            else:
                raise ValueError('{obj.__class__.__name__} db name {db_name} not exist.'.format(
                    obj=self, db_name=db_name
                ))

    @staticmethod
    def get_db_reachability():
        db_reachability_path = '/reachability'
        ref = db.reference(db_reachability_path)
        db_obj = ref.get()
        logger.debug('get_db_availability({db_path}): {db_obj}'.format(
            db_path=db_reachability_path, db_obj=db_obj
        ))
        return db_obj

    @staticmethod
    def get_dev_info(pi_serial):
        db_dev_path = '/devices/{pi_serial}/'.format(pi_serial=pi_serial)
        ref = db.reference(db_dev_path)
        db_obj = ref.get()
        logger.debug('get_dev_info({pi_serial}): {db_obj}'.format(
            pi_serial=pi_serial, db_obj=db_obj))
        return db_obj

    @staticmethod
    def get_dev_serial_list():
        db_ref_path = '/devices/'
        ref = db.reference(db_ref_path)
        db_devices = ref.get()
        serial_list = []
        if db_devices:
            serial_list = db_devices.keys()

        logger.debug('get_dev_serial_list: %s' % str(serial_list))
        logger.info('current db existing devices count: %s' % len(serial_list))
        return serial_list

