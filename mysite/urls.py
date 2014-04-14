from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView
from scrobble import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', RedirectView.as_view(url='/welcome')),
    url(r'^run$', views.run),
    url(r'^love$', views.love),
    url(r'^hello$', views.hello),

    
    url(r'^welcome$', TemplateView.as_view(template_name="index.html")),
    url(r'^first$', TemplateView.as_view(template_name='first.html')),
    url(r'^second$', views.auth),     
    url(r'^third$', views.record),

    url(r'^verify/$', views.verify),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

