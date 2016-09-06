from django.conf.urls import url
from core.views import (
    IndexView, RetrieveUpdateDestroyItemView, ListCreateItemView, login_view)

items_list = ListCreateItemView.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^item/(?P<pk>\d+)', RetrieveUpdateDestroyItemView.as_view()),
    url(r'^items/$', items_list),
    url(r'^login/$', login_view, name='login_view'),
]
