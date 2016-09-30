from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from expenses.views import (
    ExpensesView, UsersView)

router = SimpleRouter()
router.register(r'expenses', ExpensesView, base_name='expenses')
router.register(r'users', UsersView, base_name='users')

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
] + router.urls
