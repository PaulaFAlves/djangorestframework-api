import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoDetail(APIView):
  def get(self, request):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)

    return JsonResponse(serializer.data)

  def patch(self, request):
    data = request.data
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj, data=data, partial=True)

    if serializer.is_valid():
      serializer.save()

      return JsonResponse(serializer.data, status=200)
    
    return JsonResponse(serializer.errors, status=400)

  def delete(self, request, id):
    obj = get_object_or_404(Agendamento, id=id)
    obj.is_canceled = True
    obj.save()

    return Response(status=204)

class AgendamentoList(APIView):
  def get(self, request):
    qs = Agendamento.objects.all().filter(is_canceled=False)
    serializer = AgendamentoSerializer(qs, many=True)

    return JsonResponse(serializer.data, safe=False)

  def post(self, request):
    data = request.data
    serializer = AgendamentoSerializer(data=data)

    if serializer.is_valid():
      serializer.save()

      return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)
