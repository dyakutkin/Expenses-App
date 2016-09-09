from django.db.models import Q
from rest_framework import permissions

from core.models import Item


class PermittedItemsQuerysetMixin(object):
    def get_queryset(self):
        queryset = Item.objects.filter(user=self.request.user)
        if self.request.user.groups.filter(name='admin').exists():
            queryset = Item.objects.all()
        elif self.request.user.groups.filter(name='user_manager').exists():
            queryset = None
        return queryset


class GroupPermissionMixin(object):
    def has_permission(self, request, view):
        filters = Q()
        for group_name in self.permitted_groups:
            filters |= Q(name=group_name)
        if request.user.groups.filter(filters).exists():
            return True
        return False


class UserManagementPermission(GroupPermissionMixin, permissions.BasePermission):
    permitted_groups = ['admin', 'user_manager']

