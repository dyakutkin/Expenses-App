from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from expenses.views import (
    ExpensesView, FilteredExpensesView, UsersView,
    login_view, csrf_token_view)

router = SimpleRouter()
router.register(r'expenses', ExpensesView, base_name='expenses')
router.register(r'users', UsersView, base_name='users')

urlpatterns = [
    url(r'^expenses/filter/$', FilteredExpensesView.as_view()),

    url(r'^csrf/$', csrf_token_view),
    url(r'^login/$', login_view, name='login_view'),
] + router.urls
