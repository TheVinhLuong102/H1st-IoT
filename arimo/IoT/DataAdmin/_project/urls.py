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
from django.views.generic.base import RedirectView

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from arimo.IoT.DataAdmin.base.autocompletes import \
    EquipmentDataFieldAutoComplete, \
    EquipmentUniqueTypeGroupAutoComplete, \
    EquipmentUniqueTypeAutoComplete, \
    EquipmentFacilityAutoComplete, \
    EquipmentInstanceAutoComplete
from arimo.IoT.DataAdmin.base.urls import \
    ROUTER as BASE_ROUTER, \
    URL_PATTERNS as BASE_URL_PATTERNS

from arimo.IoT.DataAdmin.PredMaint.autocompletes import \
    EquipmentProblemTypeAutoComplete, \
    EquipmentProblemPeriodAutoComplete
from arimo.IoT.DataAdmin.PredMaint.urls import \
    ROUTER as PRED_MAINT_ROUTER, \
    URL_PATTERNS as PRED_MAINT_URL_PATTERNS


urlpatterns = [
    # Home Redirected URL
    url(r'^$', RedirectView.as_view(url='/admin')),

    # Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    # API URLs
    # if you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views
    # include login URLs for the browsable API
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/doc/', include_docs_urls(title='Arimo IoT DataAdmin API')),
    url(r'^api/schema/$', get_schema_view(title='Arimo IoT DataAdmin API')),

    # wire up our API using automatic URL routing
    # note that the URL path can be whatever you want
    url(r'^api/base/', include(BASE_ROUTER.urls)),
    url(r'^api/pred-maint/', include(PRED_MAINT_ROUTER.urls)),

    # Auto-Complete URLs
    url(r'^{}/$'.format(EquipmentDataFieldAutoComplete.name),
        EquipmentDataFieldAutoComplete.as_view(),
        name=EquipmentDataFieldAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeGroupAutoComplete.name),
        EquipmentUniqueTypeGroupAutoComplete.as_view(),
        name=EquipmentUniqueTypeGroupAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeAutoComplete.name),
        EquipmentUniqueTypeAutoComplete.as_view(),
        name=EquipmentUniqueTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentFacilityAutoComplete.name),
        EquipmentFacilityAutoComplete.as_view(),
        name=EquipmentFacilityAutoComplete.name),

    url(r'^{}/$'.format(EquipmentInstanceAutoComplete.name),
        EquipmentInstanceAutoComplete.as_view(),
        name=EquipmentInstanceAutoComplete.name),

    url(r'^{}/$'.format(EquipmentProblemTypeAutoComplete.name),
        EquipmentProblemTypeAutoComplete.as_view(),
        name=EquipmentProblemTypeAutoComplete.name),

    url(r'^{}/$'.format(EquipmentProblemPeriodAutoComplete.name),
        EquipmentProblemPeriodAutoComplete.as_view(),
        name=EquipmentProblemPeriodAutoComplete.name)

] + BASE_URL_PATTERNS + PRED_MAINT_URL_PATTERNS


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))
