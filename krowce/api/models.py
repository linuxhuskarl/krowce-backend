import uuid
import datetime
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created', default=datetime.datetime.utcnow)
    died_at = models.DateTimeField('date last died', null=True, blank=True)

    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Sentence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.text}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    users = models.ManyToManyField('User')

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField('key', max_length=255)
    x = models.FloatField('distance <0, >')
    y = models.FloatField('height <-4, 4>')

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.session.name} - {self.user.name} - {self.key}"
