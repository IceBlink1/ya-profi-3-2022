import random

from django.db import models


class Promo(models.Model):
    name = models.TextField()
    description = models.TextField()


class Result(models.Model):
    winner_id = models.IntegerField()
    prize_id = models.IntegerField()


class Participant(models.Model):
    name = models.TextField()
    promos_part = models.ForeignKey(Promo, on_delete=models.CASCADE, null=True, related_name='participants')


class Prize(models.Model):
    description = models.TextField()
    promos_prize = models.ForeignKey(Promo, on_delete=models.CASCADE, null=True, related_name='prizes')
