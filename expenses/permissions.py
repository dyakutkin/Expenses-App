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

    def has_object_permission(self, request, view, obj):
        if obj.groups.filter(name='user').exists():
            return True
        return False


class ExpensesPermission(GroupPermissionMixin, permissions.BasePermission):
    permitted_groups = ['admin', 'user']

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='user').exists():
            return obj.user == request.user
        return True
