from django.test import TestCase, Client
from agenda.models import Agendamento
from django.utils import timezone



class TestAgendamento(TestCase):
  def test_lista_agendamentos(self):
    client = Client()
    response = client.get('/api/agendamentos/')
    self.assertEqual(response.status_code, 200)

  def test_cria_agendamento(self):
    agendamento = Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444")
    agendamento.save()

    client = Agendamento.objects.get(nome_cliente="PAula")

    self.assertEqual(client.nome_cliente, "PAula")

  def test_agendamento_tem_atributo_is_canceled_false_quando_criado(self):
    agendamento = Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444")
    agendamento.save()

    client = Agendamento.objects.get(nome_cliente="PAula")

    self.assertFalse(client.is_canceled)

  def test_atributo_is_canceled_true_quando_agendamento_cancelado(self):
    agendamento = Agendamento.objects.create(data_horario=timezone.now(), nome_cliente="PAula", email_cliente="paula@email.com", telefone_cliente="444")
    agendamento.save()

    client = Agendamento.objects.get(nome_cliente="PAula")
    response = self.client.delete(f'/api/agendamentos/{client.id}/')
    self.assertEqual(response.status_code, 204)

    client = Agendamento.objects.get(id=client.id)
    self.assertTrue(client.is_canceled)

