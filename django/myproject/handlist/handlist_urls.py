from django.conf.urls.defaults import *

# setup 'data browse'
from django.contrib import databrowse
from handlist.models import Characters, CharacterStates

databrowse.site.register(Characters)
databrowse.site.register(CharacterStates)
# end 'data browse'

urlpatterns = patterns('webapps.handlist.views',
	(r'^$', 'index'),
	(r'^faq/$', 'faq'),
	(r'^add_data/$', 'add_data'),	
	(r'^query/$', 'query'),
	(r'^result/$', 'result'),
	(r'^chars/$', 'chars'),
	(r'^index_2/$', 'index_2'),
	#(r'^databrowse/(.*)', databrowse.site.root),
)
