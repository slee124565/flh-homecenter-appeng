
from config_provider import get_config


class AuthStore(object):

    auth_store = None

    @classmethod
    def get_auth_store(self):
        """
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

        :return: Auth
        """
        if self.auth_store is not None:
            return self.auth_store

        config = get_config()
        self.auth_store = {
            'clients': {},
            'tokens': {},
            'users': {},
        }

        self.auth_store['clients'][config.get('google_client_id')] = {
            'client_id': config.get('google_client_id'),
            'client_secret': config.get('google_client_secret')
        }

        return self.auth_store

    def generate_auth_code(self, uid, client_id):
        auth_code = 'random_hex'