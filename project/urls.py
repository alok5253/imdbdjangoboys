from django.conf.urls import patterns, include, url
from imdb import views

from django.contrib import admin
admin.autodiscover()
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^movies/$', views.MovieList.as_view(), name="movie-list"),
    url(r'^movies/(?P<pk>[0-9]+)$', views.MovieDetail.as_view(), name="movie-detail"),
    url(r'^movies/search$', views.MovieFilterList.as_view(), name="movie-filter"),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
)

urlpatterns = format_suffix_patterns(urlpatterns)