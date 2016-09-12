from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from expenses.views import (
    IndexView, ExpensesView, FilteredExpensesView, UsersView,
    login_view)

router = SimpleRouter()
router.register(r'expenses', ExpensesView, base_name='expenses')
router.register(r'users', UsersView, base_name='users')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', login_view, name='login_view'),

    url(r'^expenses/filter/$', FilteredExpensesView.as_view()),
] + router.urls
