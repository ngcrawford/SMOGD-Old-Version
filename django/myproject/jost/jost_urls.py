from django.conf.urls.defaults import *

urlpatterns = patterns('myproject.jost.views',
	(r'^$', 'index'),
	#(r'^databrowse/(.*)', databrowse.site.root),
)
