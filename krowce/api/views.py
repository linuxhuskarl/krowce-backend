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


class ScoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scores to be viewed or edited.
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


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
    data, error = parse_json_request(request)
    if error:
        return error

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse(
            {'error': 'Request lacks required fields: username, password'},
            status=400)

    user = User.objects.get(name=username)
    if user and user.password == password:
        return JsonResponse({})
    return JsonResponse({'error': 'Wrong credentials'}, status=401)


@require_POST
def signup(request: HttpRequest) -> HttpResponse:
    data, error = parse_json_request(request)
    if error:
        return error

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
    team: Team = get_object_or_404(Team, name=teamname)
    if not team:
        return JsonResponse(
            {'error': 'Team with specified name does not exist'}, status=400)

    user, created = User.objects.get_or_create(name=username,
                                               password=password,
                                               team=team)
    user.save()
    if created:
        return JsonResponse({}, status=201)
    return JsonResponse({})


@require_POST
def join_session(request: HttpRequest) -> HttpResponse:
    data, error = parse_json_request(request)
    if error:
        return error

    username = data.get('username')
    sessionname = data.get('session', 'default')
    if not username or not sessionname:
        return JsonResponse(
            {'error': 'Request lacks required fields: username, session'},
            status=400)
    session: Session = get_object_or_404(Session, name=sessionname)
    user: user = get_object_or_404(User, name=username)
    if not user in session.users.all():
        session.users.add(user)
    return JsonResponse({})


@require_POST
def add_item_sentence_and_score(request: HttpRequest) -> HttpResponse:
    data, error = parse_json_request(request)
    if error:
        return error

    username = data.get('user')
    sessionname = data.get('session', 'default')
    text = data.get('text')
    item_key = data.get('key')
    item_x = data.get('x', 0)
    item_y = data.get('y', 0)
    dist = data.get('score', 0)

    if not username or not text or not item_key:
        return JsonResponse(
            {'error': 'Request lacks required fields: username, text, key'},
            status=400)

    session: Session = get_object_or_404(Session, name=sessionname)

    try:
        user = User.objects.get(name=username)
    except User.DoesNotExist:
        user = User(name=username)
        user.team = Team.objects.get(name='Krowy')
        user.save()
        session.users.add(user)

    sentence = Sentence()
    sentence.text = text
    sentence.user = user
    sentence.save()

    item = Item()
    item.key = item_key
    item.x = item_x
    item.y = item_y
    item.user = user
    item.session = session
    item.sentence = sentence
    item.save()

    score = Score()
    score.user = user
    score.distance = dist
    score.session = session
    score.save()

    return JsonResponse({})


def parse_json_request(request: HttpRequest) -> tuple[dict, dict]:
    if request.content_type != 'application/json':
        return None, JsonResponse({'error': 'Invalid content type'}, status=400)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return data, None
