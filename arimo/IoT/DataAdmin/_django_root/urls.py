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

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

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
    url(r'^api/doc/', include_docs_urls(title='Arimo IoT REST API')),
    url(r'^api/schema/$', get_schema_view(title='Arimo IoT REST API')),

    # Silk Profiling URLs
    url(r'^silk/', include('silk.urls', namespace='silk'))

] + BASE_URL_PATTERNS + PRED_MAINT_URL_PATTERNS
