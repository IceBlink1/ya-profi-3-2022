import random

from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .serialiazers import *


@csrf_exempt
def promo_list(request):
    if request.method == 'GET':
        promos = Promo.objects.all()
        serializer = SimplePromoSerializer(promos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SimplePromoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data['id'], status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)


@csrf_exempt
def promo_by_id(request, pk):
    try:
        promo = Promo.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PromoSerializer(promo)
        return JsonResponse(serializer.data)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SimplePromoSerializer(promo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)
    if request.method == 'DELETE':
        promo.delete()
        return HttpResponse(status=204)


@csrf_exempt
def promo_by_id_post_participant(request, pk):
    try:
        promo = Promo.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        part_serializer = ParticipantSerializer(data=data)
        if part_serializer.is_valid():
            participant = part_serializer.save()
            promo.participants.add(participant)
            participant.save()
            promo.save()
            return JsonResponse(participant.id, status=201, safe=False)
        return HttpResponse(status=400)


@csrf_exempt
def promo_by_id_participant(request, pk, participant_pk):
    try:
        promo = Promo.objects.get(pk=pk)
        participant = promo.participants.objects.get(participant_pk)
    except:
        return HttpResponse(status=404)
    if request.method == 'DELETE':
        participant.delete()
        return HttpResponse(status=204)


@csrf_exempt
def promo_by_id_post_prize(request, pk):
    try:
        promo = Promo.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        prize_serializer = PrizeSerializer(data=data)
        if prize_serializer.is_valid():
            prize = prize_serializer.save()
            promo.prizes.add(prize)
            prize.save()
            promo.save()
            return JsonResponse({'id': prize.id}, status=201, safe=False)


@csrf_exempt
def promo_by_id_prize(request, pk, prize_pk):
    try:
        promo = Promo.objects.get(pk=pk)
        prize = promo.prizes.objects.get(prize_pk)
    except:
        return HttpResponse(status=404)
    if request.method == 'DELETE':
        prize.delete()
        return HttpResponse(status=204)


@csrf_exempt
def raffle(request, pk):
    try:
        promo = Promo.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        prizes = promo.prizes.all()
        participants = promo.participants.all()
        if participants.count() != prizes.count():
            return HttpResponse(status=409)
        prizes_list = list(prizes)
        participants_list = list(participants)
        random.shuffle(prizes_list)
        l = []
        for i in range(len(prizes_list)):
            res = Result.objects.create(winner_id=participants_list[i].pk, prize_id=prizes_list[i].pk)
            res.save()
            l.append(res)
        res_ser = ResultSerializer(l, many=True)
        return JsonResponse(res_ser.data, status=201, safe=False)
