from django.conf.urls import url
from . import views           
urlpatterns = [
	url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$',views.books),
    url(r'^logout$',views.logout),
    url(r'^books/(?P<id>\d+)$',views.showbook),
    url(r'^books/add$',views.addpage),
    url(r'^addbookprocess$',views.addbookprocess),
    url(r'^addreviewprocess/(?P<id>\d+)$', views.addreviewprocess),
    url(r'^users/(?P<id>\d+)$',views.profile),
    url(r'^delete/(?P<id>\d+)$',views.deletereview)
]
