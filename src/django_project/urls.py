from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^web/',include('web.urls', namespace="web")),
    url(r'^merge/', 'web.views.merge'),
]
