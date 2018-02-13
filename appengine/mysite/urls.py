"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
# from django.views.decorators.csrf import csrf_exempt

# from firebasedb.views import ReachabilityView as FirebaseDBReachabilityView
# from firebasedb.views import DeviceInfoView, DeviceListView

# from clients.views import ClientDevView

from backend_api.admin.views import FirebaseDBReachabilityView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # == admin backend api sub-url include ==
    url(r'^v1/a/', include('backend_api.admin.urls')),

    # == user backend api sub-url include ==
    url(r'^v1/u/', include('backend_api.firenotes.urls')),

    # == ifttt service api include ==
    url(r'^ifttt/v1/', include('backend_api.ifttt.urls')),

    # == flh service api include ==
    url(r'^s/h/', include('backend_api.services.hc2.urls')),

    # url(r'^db/dev/(?P<pi_serial>\w+)/$', DeviceInfoView.as_view(), name='dev_info'),


]
