from datetime import datetime
import json
from django.forms import ValidationError
from django.test import Client
from rest_framework.test import APITestCase
from agenda.models import Agendamento
from django.utils import timezone 
from rest_framework import serializers
from django.contrib.auth.models import User

class TestAgendamento(APITestCase):
  def test_listagem_vazia(self):
    response = self.client.get('/api/agendamentos/')
    data = json.loads(response.content)
    self.assertEqual(data, [])

  def test_lista_agendamentos(self):
    agendamentos_esperados = [{
        'id': 1, 
        'data_horario': '2022-12-12T00:00:00Z', 
        'nome_cliente': 'PAula', 
        'email_cliente': 'paula@email.com', 
        'telefone_cliente': '444',
        'prestador': 'admin',
        'is_canceled': False
        }
      ]

    Agendamento.objects.create(data_horario=datetime(2022, 12, 12, tzinfo=timezone.utc), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=User.objects.create(username='admin'))

    client = Client()
    response = client.get('/api/agendamentos/?username=admin')
    data = json.loads(response.content)

    self.assertEqual(len(data), 1)
    self.assertEqual(data, agendamentos_esperados)

  def test_quando_request_retorna_400(self):
    User.objects.create(username='admin')
    client = Client()
    response = client.post('/api/agendamentos/', {'data_horario':'2020-12-12T00:00:00Z', 'nome_cliente':"PAula", 'email_cliente':"paula@email.com", 'telefone_cliente':"444", "prestador":"admin"})
    self.assertEqual(response.status_code, 400)

    data = json.loads(response.content)
    self.assertEqual(data, {'data_horario': ['Agendamento não pode ser feito no passado.']})

  def test_cria_agendamento(self):
    Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=User.objects.create(username='admin'))

    client = Agendamento.objects.get(nome_cliente="PAula")

    self.assertEqual(client.nome_cliente, "PAula")

  def test_agendamento_tem_atributo_is_canceled_false_quando_criado(self):
    Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=User.objects.create(username='admin'))

    client = Agendamento.objects.get(nome_cliente="PAula")

    self.assertFalse(client.is_canceled)

  def test_atributo_is_canceled_true_quando_agendamento_cancelado(self):
    Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=User.objects.create(username='admin'))

    client = Agendamento.objects.get(nome_cliente="PAula")
    response = self.client.delete(f'/api/agendamentos/{client.id}/')
    self.assertEqual(response.status_code, 204)

    client = Agendamento.objects.get(id=client.id)
    self.assertTrue(client.is_canceled)