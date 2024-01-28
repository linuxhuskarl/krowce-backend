from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='name',
                                        queryset=Team.objects.all())
    scores = serializers.SlugRelatedField(many=True,
                                          source='score_set',
                                          slug_field='distance',
                                          read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'team', 'created_at', 'died_at', 'scores']

class ItemSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', queryset=User.objects.all())
    sentence = serializers.SlugRelatedField(read_only=True, slug_field='text')
    class Meta:
        model = Item
        fields = ['id', 'key', 'x', 'y', 'disables', 'lane', 'user', 'sentence']


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', queryset=User.objects.all())
    team = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = ['id', 'user', 'team', 'distance']

    def get_team(self, score: Score):
        return score.user.team.name


class SessionSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(many=True,
                                         slug_field='name',
                                         queryset=User.objects.all())
    items = ItemSerializer(many=True, read_only=True, source='item_set')
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'name', 'users', 'items', 'scores']

    def get_scores(self, session: Session):
        scores = session.score_set.order_by('-distance')
        return ScoreSerializer(scores, many=True).data


class TeamSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True, source='user_set') #UserSerializer(many=True, read_only=True, source='user_set')
    class Meta:
        model = Team
        fields = ['id', 'name', 'users']
