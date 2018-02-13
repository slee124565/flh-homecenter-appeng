
from django.conf.urls import url

from .endpoints import IFTTTStatusEndPoint
from .endpoints import IFTTTTestSetupEndPoint
# from .endpoints import IFTTTTestNewThingCreatedTrigger
from .endpoints import IFTTTStartHC2SceneAction

urlpatterns = [

    # == backend api for admin start ==
    url(r'^status', IFTTTStatusEndPoint.as_view(), 'ifttt.status.endpoint'),
    url(r'^test/setup', IFTTTTestSetupEndPoint.as_view(), 'ifttt.test.setup'),
    # url(r'^triggers/new_thing_created', IFTTTTestNewThingCreatedTrigger.as_view(), 'ifttt.trigger.new_thing_created'),
    url(r'^actions/start_hc2_scene', IFTTTStartHC2SceneAction.as_view(), 'ifttt.action.start_hc2_scene'),

]

