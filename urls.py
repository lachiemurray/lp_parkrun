from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^edition/$', 'lp_hello_django.views.edition'),
    url(r'^sample/$', 'lp_hello_django.views.sample'),
    url(r'^validate_config/$', 'lp_hello_django.views.validate_config'),
    url(r'^configure/$', 'lp_hello_django.views.configure'),
    url(r'^meta.json$', 'lp_hello_django.views.meta_json'),
    url(r'^icon.png$', 'lp_hello_django.views.icon'),
    
)




