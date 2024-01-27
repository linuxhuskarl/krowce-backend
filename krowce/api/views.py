import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *


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

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SessionSerializer(queryset, many=True)
        return Response({"sessions": serializer.data})


@require_POST
def login(request: HttpRequest) -> HttpResponse:
    # Check if the request contains JSON data
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    # Parse the JSON data
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse(
            {'error': 'Request lacks required fields: username, password'},
            status=400)

    user = User.objects.get(name=username)
    if user and user.password == password:
        return JsonResponse({}, status=200)
    return JsonResponse({'error': 'Wrong credentials'}, status=401)


@require_POST
def signup(request: HttpRequest) -> HttpResponse:
    # Check if the request contains JSON data
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Invalid content type'}, status=400)

    # Parse the JSON data
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    username = data.get('username')
    password = data.get('password')
    teamname = data.get('team')
    if not username or not password or not teamname:
        return JsonResponse(
            {
                'error':
                'Request lacks required fields: username, password, teamname'
            },
            status=400)
    team = get_object_or_404(Team, name=teamname)
    if not team:
        return JsonResponse(
            {'error': 'Team with specified name does not exist'}, status=400)

    user, created = User.objects.get_or_create(name=username,
                                               password=password,
                                               team=team)
    user.save()
    if created:
        return JsonResponse({}, status=201)
    return JsonResponse({}, status=200)
