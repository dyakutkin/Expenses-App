from django.db.models import Q
from rest_framework import permissions


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


class ExpensesPermission(GroupPermissionMixin, permissions.BasePermission):
    permitted_groups = ['admin', 'user']
