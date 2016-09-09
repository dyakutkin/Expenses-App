from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.db.models import Q

from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from core.permissions import PermittedItemsQuerysetMixin, UserManagementPermission

from core.models import Item
from core.serializers import (ItemSerializer, ItemFilterSerializer, UserSerializer)


def login_view(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserManagementPermission]


class RetrieveUpdateDestroyItemView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (BasicAuthentication,)


class ListCreateItemView(PermittedItemsQuerysetMixin, ModelViewSet):
    serializer_class = ItemSerializer

    def create(self, serializer):
        data = self.request.data.copy()
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        return HttpResponse(status=400)


class FilteredItemsView(PermittedItemsQuerysetMixin, APIView):
    def get(self, request):
        filter_serializer = ItemFilterSerializer(data=request.GET)
        filter_serializer.is_valid(raise_exception=True)

        filters = Q()

        date_from = filter_serializer.validated_data.get('date_from')
        if date_from:
            filters &= Q(date__gte=date_from)

        date_to = filter_serializer.validated_data.get('date_to')
        if date_to:
            filters &= Q(date__lte=date_to)

        time_from = filter_serializer.validated_data.get('time_from')
        if time_from:
            filters &= Q(time__gte=time_from)

        time_to = filter_serializer.validated_data.get('time_to')
        if time_to:
            filters &= Q(time__lte=time_to)

        queryset = Item.objects.filter(filters)
        items_serializer = ItemSerializer(queryset, many=True)
        return Response(data=items_serializer.data)
