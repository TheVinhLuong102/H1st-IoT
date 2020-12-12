from django.urls.conf import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

from arimo.IoT.DataAdmin.base.urls import URL_PATTERNS as BASE_URLS
from arimo.IoT.DataAdmin.PredMaint.urls import URL_PATTERNS as PRED_MAINT_URLS


admin.site.index_title = 'Arimo'
admin.site.site_title = 'IoT'
admin.site.site_header = 'Arimo IoT'


urlpatterns = [
    # Home URL Redirected to Admin
    path('', RedirectView.as_view(url='/admin')),
    path('admin/', admin.site.urls),

    # API URLs
    path('api/auth/',
         include('rest_framework.urls', namespace='rest_framework')),

    # Silk Profiling URLs
    path('silk/',
         include('silk.urls', namespace='silk'))

] + BASE_URLS + PRED_MAINT_URLS
