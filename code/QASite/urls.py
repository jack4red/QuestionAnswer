from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('QuestionAnswer.urls')),
    url(r'^QuestionAnswer/', include('QuestionAnswer.urls')),
    url(r'^account/', include('account.urls')),
)
