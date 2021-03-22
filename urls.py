from django.urls.conf import include, path
from django.contrib import admin
from django.views.generic.base import RedirectView

from h1st.IoT.DataAdmin.base.urls import URL_PATTERNS as BASE_URLS
from h1st.IoT.DataAdmin.PredMaint.urls import URL_PATTERNS as PRED_MAINT_URLS


admin.site.index_title = 'H1st'
admin.site.site_title = 'IoT'
admin.site.site_header = 'H1st IoT'


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
