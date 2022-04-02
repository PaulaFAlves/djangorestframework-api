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
    user = User.objects.create(email="bob@email.com", username="bob", password="123")
    self.client.force_authenticate(user)

    response = self.client.get('/api/agendamentos/?username=bob')
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

    user = User.objects.create(email="bob@email.com", username="admin", password="123")
    Agendamento.objects.create(data_horario=datetime(2022, 12, 12, tzinfo=timezone.utc), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=user)

    self.client.force_authenticate(user)
    response = self.client.get('/api/agendamentos/?username=admin')
    data = json.loads(response.content)

    self.assertEqual(len(data), 1)
    self.assertEqual(data, agendamentos_esperados)

  def test_quando_request_retorna_400(self):
    User.objects.create(username='admin')
    response = self.client.post('/api/agendamentos/', {'data_horario':'2020-12-12T00:00:00Z', 'nome_cliente':"PAula", 'email_cliente':"paula@email.com", 'telefone_cliente':"444", "prestador":"admin"})
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
    user = User.objects.create(email="bob@email.com", username="admin", password="123")
    Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=user)

    client = Agendamento.objects.get(nome_cliente="PAula")

    self.client.force_authenticate(user)

    response = self.client.delete(f'/api/agendamentos/{client.id}/')
    self.assertEqual(response.status_code, 204)

    client = Agendamento.objects.get(id=client.id)
    self.assertTrue(client.is_canceled)
    

  def test_prestador_nao_existe(self):
    User.objects.create(username='admin')
    response = self.client.post('/api/agendamentos/', {'data_horario':'2023-12-12T14:00:00Z', 'nome_cliente':"PAula", 'email_cliente':"paula@email.com", 'telefone_cliente':"444", "prestador":"bob"})

    self.assertEqual(response.status_code, 400)
    
    data = json.loads(response.content)
    self.assertEqual(data, {'prestador': ['Prestador não existe']})

  def test_prestador_nao_autorizado(self):
    user = User.objects.create(email="bob@email.com", username="admin", password="123")
    user2 = User.objects.create(email="bob@email.com", username="bob", password="123")

    client = Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444", prestador=user)

    self.client.force_authenticate(user)

    response = self.client.get(f'/api/agendamentos/?username=admin/')
    self.assertEqual(response.status_code, 403)

    data = json.loads(response.content)
    self.assertEqual(data, {'detail': 'You do not have permission to perform this action.'})

class TestGetHorarios(APITestCase):
  def test_quando_data_e_feriado_retorna_lista_vazia(self):
    response = self.client.get("/api/horarios/?data=2022-12-25")
    data = json.loads(response.content)
    self.assertEqual(data, [])

  def test_quando_data_nao_e_feriado_retorna_lista_cheia(self):
    response = self.client.get("/api/horarios/?data=2022-12-12")
    data = json.loads(response.content)
    self.assertNotEqual(data, [])
    self.assertEqual(data[0], '2022-12-12T09:00:00Z')
    self.assertEqual(data[-1], '2022-12-12T17:30:00Z')