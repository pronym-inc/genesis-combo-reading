from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import re_path, path, include


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',
        include(
            ('genesis_combo_reading.apps.core.urls',
             'genesis_combo_reading.apps.core'),
            namespace='core')
    ),
]

if settings.DEBUG_STATIC_FILES:
    urlpatterns += [re_path(r'^devstatic/(?P<path>.*)$', serve)]
