from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group as AuthGroup, User as AuthUser
from rest_framework import permissions, viewsets
from .serializers import *
from .models import *



# Create your views here.
def echo_response(request: HttpRequest) -> HttpResponse:
    # get the message from the request and return it as is
    message = request.GET.get('msg', 'No message provided.')

    return HttpResponse(f"echo: {message}")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sessions to be viewed or edited.
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer