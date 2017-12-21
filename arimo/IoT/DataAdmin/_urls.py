from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from arimo.IoT.DataAdmin.base.autocompletes import EquipmentDataFieldAutoComplete, EquipmentUniqueTypeAutoComplete


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin')),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^{}/$'.format(EquipmentDataFieldAutoComplete.name),
        EquipmentDataFieldAutoComplete.as_view(),
        name=EquipmentDataFieldAutoComplete.name),

    url(r'^{}/$'.format(EquipmentUniqueTypeAutoComplete.name),
        EquipmentUniqueTypeAutoComplete.as_view(),
        name=EquipmentUniqueTypeAutoComplete.name)
]
