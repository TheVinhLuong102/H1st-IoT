"""URL Configuration

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

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView

from rest_framework import routers, serializers, viewsets

from arimo.IoT.DataAdmin.base.autocompletes import \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentUniqueTypeAutoComplete, \
    EquipmentInstanceAutoComplete
from arimo.IoT.DataAdmin.PredMaint.autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentProblemPeriodAutoComplete


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin')),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', admin.site.urls),

    # wire up our API using automatic URL routing
    # note that the URL path can be whatever you want
    url(r'^rest/', include(router.urls)),

    # if you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views
    # include login URLs for the browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^{}/$'.format(EquipmentDataFieldAutoComplete.name),
        EquipmentDataFieldAutoComplete.as_view(),
        name=EquipmentDataFieldAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeGroupAutoComplete.name),
        EquipmentUniqueTypeGroupAutoComplete.as_view(),
        name=EquipmentUniqueTypeGroupAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeAutoComplete.name),
        EquipmentUniqueTypeAutoComplete.as_view(),
        name=EquipmentUniqueTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentInstanceAutoComplete.name),
        EquipmentInstanceAutoComplete.as_view(),
        name=EquipmentInstanceAutoComplete.name),

    url(r'^{}/$'.format(EquipmentProblemTypeAutoComplete.name),
        EquipmentProblemTypeAutoComplete.as_view(),
        name=EquipmentProblemTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentProblemPeriodAutoComplete.name),
        EquipmentProblemPeriodAutoComplete.as_view(),
        name=EquipmentProblemPeriodAutoComplete.name)
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
