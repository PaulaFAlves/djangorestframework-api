from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList, get_horarios, healthcheck, relatorio_prestadores

urlpatterns = [
     path('agendamentos/', AgendamentoList.as_view()),
     path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
     path('prestadores/', relatorio_prestadores),
     path('horarios/', get_horarios),
     path('', healthcheck)
]
