from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

@api_view(http_method_names=["GET"])
def agendamento_detail(request, id):
  obj = get_object_or_404(Agendamento, id=id)
  serializer = AgendamentoSerializer(obj)

  return JsonResponse(serializer.data)

@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
  if request.method == 'GET':
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializer(qs, many=True)

    return JsonResponse(serializer.data, safe=False)

  if request.method == "POST":
    data = request.data
    serializer = AgendamentoSerializer(data=data)

    if serializer.is_valid():
      valitated_data = serializer.validated_data
      Agendamento.objects.create(
        data_horario=valitated_data["data_horario"],
        nome_cliente=valitated_data["nome_cliente"],
        email_cliente=valitated_data["email_cliente"],
        telefone_cliente=valitated_data["telefone_cliente"],
      )

      return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)
