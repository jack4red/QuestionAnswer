from django.conf.urls import patterns, include, url
from django.contrib import admin
from QASite import views
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('QuestionAnswer.urls')),
    url(r'^QuestionAnswer/', include('QuestionAnswer.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^upload_rich_text_image/$', views.upload_rich_text_image),
)
