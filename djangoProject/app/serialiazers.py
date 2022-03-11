from rest_framework import serializers
from .models import *


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name']


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ['id', 'description']


class PromoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    prizes = PrizeSerializer(many=True, required=False, default=None)
    participants = ParticipantSerializer(many=True, required=False, default=None)

    class Meta:
        model = Promo
        fields = ['id', 'name', 'description', 'prizes', 'participants']


class SimplePromoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Promo
        fields = ['id', 'name', 'description']


class ResultSerializer(serializers.ModelSerializer):
    prize = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()#ParticipantSerializer(many=False, required=False)


    def get_prize(self, obj):
        return PrizeSerializer(Prize.objects.get(pk=obj.prize_id)).data

    def get_winner(self, obj):
        return ParticipantSerializer(Participant.objects.get(pk=obj.prize_id)).data
    class Meta:
        model = Result
        fields = ['prize', 'winner']
