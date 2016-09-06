from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, reverse, HttpResponse

from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drf_roles.mixins import RoleViewSetMixin

from models import Item
from serializers import ItemSerializer


def login_view(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponse('Cool')

    return redirect(reverse('index'))


class IndexView(TemplateView):
    template_name = 'index.html'


class RetrieveUpdateDestroyItemView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (BasicAuthentication,)


class ListCreateItemView(RoleViewSetMixin, ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        print '****user: ', self.request.user
        return Item.objects.filter(user=self.request.user)

    def create(self, serializer):
        data = self.request.data.copy()
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)


class ListCreateItemView1(ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(self.request.user)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
