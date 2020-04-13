from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.views import generic
from django.conf.urls import include
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^new/$', views.new, name='new'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^item/(?P<pk>\d+)$', views.ask_ind, name='ask_ind'),
    url(r'^like', views.like2),
    url(r'^dislike', views.dislike),
    url('', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    url(r'^user/(?P<pk>\d+)$', views.userpage, name='userpage'),
    url(r'^user/submits/(?P<pk>\d+)$', views.sub_user, name='sub_user'),
    url(r'^user/comments/(?P<pk>\d+)$', views.com_user, name='com_user'),
    url(r'^user/likes/(?P<pk>\d+)$', views.lik_user, name='lik_user'),


]
