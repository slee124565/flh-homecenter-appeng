
import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
from backend_api.services.hc2 import apis
apis.FlhHc2SceneControlAPI.api_test()