from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User

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

class PrestadorList(generics.ListAPIView):
  serializer_class = PrestadorSerializer
  queryset = User.objects.all()

  