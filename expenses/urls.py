from django.conf.urls import url
from expenses.views import (
    IndexView, RetrieveUpdateDestroyExpenseView, ListCreateItemView, FilteredExpensesView, UsersView,
    login_view)

items_list = ListCreateItemView.as_view({
    'get': 'list',
    'post': 'create',
})

users_list = UsersView.as_view({
    'get': 'list',
    'post': 'create'
})

users_detail = UsersView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', login_view, name='login_view'),

    url(r'^item/(?P<pk>\d+)', RetrieveUpdateDestroyExpenseView.as_view()),
    url(r'^items/$', items_list),
    url(r'^items/filter/$', FilteredExpensesView.as_view()),

    url(r'^users/$', users_list),
    url(r'^user/(?P<pk>\d+)', users_detail),
]
