from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^handlist/', include('myproject.handlist.handlist_urls')),  # include 'handlist_urls'
	(r'^jost/', include('myproject.jost.jost_urls')),  # include 'handlist_urls'
)

urlpatterns += patterns( '',
	# path do media (e.g. images, style sheets, java script, etc...)
	#(r'^web-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/nick/Web_Design/django_templates/media'}),
	(r'^web_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/alchemist/Projects/SMOGD-Old-Version/web_media'}),
)


