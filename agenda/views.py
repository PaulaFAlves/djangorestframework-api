import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from rest_framework import mixins
from rest_framework import generics

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer

  def perform_destroy(self, instance):
    instance.is_canceled = True
    instance.save()
class AgendamentoList(generics.ListCreateAPIView):
  serializer_class = AgendamentoSerializer

  def get_queryset(self):
    username = self.request.query_params.get('username', None)
    queryset = Agendamento.objects.filter(prestador__username=username)
    return queryset