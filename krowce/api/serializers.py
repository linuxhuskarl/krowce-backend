from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'team']

class ItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    sentence = serializers.SlugRelatedField(read_only=True, slug_field='text')

    class Meta:
        model = Item
        fields = ['id', 'key', 'x', 'y', 'user', 'sentence']


class SessionSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True, source='item_set')
    class Meta:
        model = Session
        fields = ['id', 'name', 'users', 'items']




class TeamSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True, source='user_set')

    class Meta:
        model = Team
        fields = ['id', 'name', 'users']
