# Generated by Django 4.0.2 on 2022-03-17 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='data_horario',
            field=models.DateTimeField(),
        ),
    ]
