from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/client/charge[/]*$', 'sivams.payments.views.client_charge', name='client_charge'),
    url(r'^admin/client/invoice[/]*$', 'sivams.payments.views.invoice', name='client_invoice'),
    url(r'^[/]*$', 'sivams.app.views.home', name='construction'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^about[/]*$', 'sivams.app.views.about', name='about'),
    url(r'^services[/]*$', 'sivams.app.views.services', name='services'),
    url(r'^contact[/]*$', 'sivams.app.views.contact', name='contact'),
    url(r'^gallery[/]*$', 'sivams.app.views.gallery', name='gallery'),
    url(r'^publications[/]*$', 'sivams.app.views.publications', name='publications'),
    url(r'^dev[/]*$', 'sivams.app.views.home', name='home'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^dev/about[/]*$', 'sivams.app.views.about', name='about'),
    url(r'^dev/services[/]*$', 'sivams.app.views.services', name='services'),
    url(r'^dev/contact[/]*$', 'sivams.app.views.contact', name='contact'),
    url(r'^dev/gallery[/]*$', 'sivams.app.views.gallery', name='gallery'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.PROJECT_ROOT + '/templates'}),
    # Examples:
    # url(r'^$', 'sivams.views.home', name='home'),
    # url(r'^sivams/', include('sivams.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
