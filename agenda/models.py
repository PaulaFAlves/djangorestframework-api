from django.db import models

class Agendamento(models.Model):
  prestador = models.ForeignKey('auth.user', related_name='agendamentos', on_delete=models.CASCADE)

  data_horario = models.DateTimeField()
  nome_cliente = models.CharField(max_length=200)
  email_cliente = models.EmailField()
  telefone_cliente = models.CharField(max_length=20)
  is_canceled = models.BooleanField(default=False)

  def __str__(self):
      return f"{self.nome_cliente} - {self.id}"