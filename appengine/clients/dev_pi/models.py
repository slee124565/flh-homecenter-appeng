# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.db import models

from firebasedb.models import FirebaseDB

import logging
logger = logging.getLogger(__name__)


def get_dev_db_obj(pi_serial):
    firebase_db = FirebaseDB()
    db_dev = firebase_db.get_dev_info(pi_serial)
    return db_dev


class DevicePi(object):

    pi_serial = None

    def __init__(self, pi_serial):
        self.pi_serial = pi_serial
        self._db_obj = get_dev_db_obj(self.pi_serial)
        if self._db_obj is None:
            raise ValueError('device ({obj.pi_serial} not exist in db)'.format(obj=self))

    def __str__(self):
        return '{obj.__class__.__name__}({obj.pi_serial})'.format(obj=self)

    def get_dev_http_url(self):
        http_tunnel = None
        if self._db_obj.get('info',{}).get('tunnels',None):
            dev_tunnels = self._db_obj.get('info',{}).get('tunnels',None)
            for tunnel in dev_tunnels:
                if tunnel.find('http://') >= 0:
                    http_tunnel = tunnel
        logger.debug('{obj} get_dev_http_url: {tunnel}'.format(obj=self, tunnel=http_tunnel))
        return http_tunnel
