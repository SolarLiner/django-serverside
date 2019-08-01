import uuid

from django.db import models


class BaseObject(models.Model):
    class Meta:
        abstract = True

    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


class Player(BaseObject):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(BaseObject):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, related_name="+", through="ScoreboardEntry")

    def __str__(self):
        return self.name


class ScoreboardEntry(BaseObject):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="scores")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores")
    score = models.PositiveIntegerField()
