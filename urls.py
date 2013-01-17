from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^edition/$', 'lp_parkrun.views.edition'),
    url(r'^sample/$', 'lp_parkrun.views.sample'),
    url(r'^validate_config/$', 'lp_parkrun.views.validate_config'),
    url(r'^configure/$', 'lp_parkrun.views.configure'),
    url(r'^meta.json$', 'lp_parkrun.views.meta_json'),
    url(r'^icon.png$', 'lp_parkrun.views.icon'),
    
)




