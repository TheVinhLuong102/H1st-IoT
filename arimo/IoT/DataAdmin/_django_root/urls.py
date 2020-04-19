from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from ..base.urls import URL_PATTERNS as BASE_URL_PATTERNS
from ..PredMaint.urls import URL_PATTERNS as PRED_MAINT_URL_PATTERNS


admin.site.index_title = 'Arimo'
admin.site.site_title = 'IoT'
admin.site.site_header = 'Arimo IoT'


urlpatterns = [
    # Home URL Redirected to Admin
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/', admin.site.urls),

    # API URLs
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Silk Profiling URLs
    url(r'^silk/', include('silk.urls', namespace='silk'))

] + BASE_URL_PATTERNS + PRED_MAINT_URL_PATTERNS
