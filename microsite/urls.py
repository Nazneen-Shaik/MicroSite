from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'microsite_front.views.index'),
    url(r'^report/$','micro_blog.views.report'),
    url(r'^contact/$','micro_blog.views.contact'),
    url(r'^careers/$','microsite_front.views.career_page'),
    url(r'^portal/', include('micro_admin.urls', namespace='micro_admin')),
    url(r'^blog/', include('micro_blog.urls', namespace='micro_blog')),
    url(r'^portal/content/', include('pages.urls', namespace='pages')),
    url(r'^portal/employee/', include('employee.urls', namespace='employee')),
    url(r'^portal/kb/', include('micro_kb.urls', namespace='micro_kb')),
    url(r'^docs/', include('docs.urls', namespace='docs')),
    url(r'^(?P<slug>[-\w]+)/$','pages.views.site_page'),
    url(r'^rss.xml$', 'microsite_front.xml.rss' ),
    url(r'^sitemap.xml$', 'microsite_front.xml.sitemap'),
)
