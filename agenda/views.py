import csv
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, HorariosSerializer, PrestadorSerializer
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes

from agenda.utils import get_horarios_disponiveis

class IsOwnerOrCreateOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == 'POST':
      return True
    
    username = request.query_params.get('username', None)
    if request.user.username == username:
      return True

    return False

class IsPrestador(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj.prestador == request.user:
      return True
    
    return False
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsPrestador]
  queryset = Agendamento.objects.all()
  serializer_class = AgendamentoSerializer

  def perform_destroy(self, instance):
    instance.is_canceled = True
    instance.save()
class AgendamentoList(generics.ListCreateAPIView):
  serializer_class = AgendamentoSerializer
  permission_classes = [IsOwnerOrCreateOnly]

  def get_queryset(self):
    username = self.request.query_params.get('username', None)
    queryset = Agendamento.objects.filter(prestador__username=username)
    return queryset

@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAdminUser])
def relatorio_prestadores(request):
  formato = request.query_params.get("formato")
  prestadores = User.objects.all()
  serializer = PrestadorSerializer(prestadores, many=True)

  if formato == "csv":
    data_hoje = date.today()
    response = HttpResponse(
      content_type='text/csv',
      headers={'Content-Disposition': f'attachment; filename="relatorio_{data_hoje}.csv'},
    )
    writer = csv.writer(response)
    for prestador in serializer.data:
      agendamentos = prestador["agendamentos"]
      for agendamento in agendamentos:
        writer.writerow([
          agendamento["prestador"],
          agendamento["nome_cliente"],
          agendamento["email_cliente"],
          agendamento["data_horario"],
        ])
    return response
  else:
    return Response(serializer.data)

@api_view(http_method_names=["GET"])
def get_horarios(request):
  data = request.query_params.get("data")
  if not data:
    data = datetime.now().date()
  else:
    data = datetime.fromisoformat(data).date()

  horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
  return JsonResponse(horarios_disponiveis, safe=False)


@api_view(http_method_names=["GET"])
def healthcheck(request):
  return Response({"status": "ok", "message": "Tudo ok"}, status=200)
