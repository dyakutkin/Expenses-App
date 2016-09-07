from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, reverse, HttpResponse

from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from models import Item
from serializers import ItemSerializer


def login_view(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponse('Cool')

    return HttpResponse('Not cool')


class IndexView(TemplateView):
    template_name = 'index.html'


class RetrieveUpdateDestroyItemView(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (BasicAuthentication,)


class ListCreateItemView(ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.filter(user=self.request.user)
        if self.request.user.groups.filter(name='admin').exists():
            queryset = Item.objects.all()
        elif self.request.user.groups.filter(name='user_manager').exists():
            queryset = None
        return queryset

    def create(self, serializer):
        data = self.request.data.copy()
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)