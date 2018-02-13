
import requests, json
import logging
logger = logging.getLogger(__name__)


class ClientHC2(object):
    secret_key = 'showroom'
    api_root_url = 'http://flhshowroom.mynetgear.com:8000'

    @staticmethod
    def get_client_by_key(client_key):
        logger.warning('TODO: implement ClientHC2.get_client_by_key')
        return ClientHC2()

    def control_hc2_scene(self, scene_name, room_name=None, lang_code='en', action='start'):
        scene_ctl_path = '/vb/i/s/'
        payload = {
            'scene_name': scene_name,
            'room_name': room_name,
            'lang_code': lang_code,
            'action': action
        }
        api_url = self.api_root_url + scene_ctl_path
        logger.debug('{obj.__class__.__name__} control_hc2_scene with {payload} and {url}'.format(
            obj=self, payload=payload, url=api_url
        ))
        r = requests.post(api_url, data=json.dumps(payload))
        if r.status_code in range(200, 300):
            return True
        else:
            logger.warning('http post fail, ({err_code}, {err_msg})'.format(
                err_code=r.status_code, err_msg=r.content
            ))
            return False
