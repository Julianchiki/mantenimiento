# Generated by Django 4.2.3 on 2023-11-14 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0003_alter_appointments_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='state',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PROCESO', 'Proceso'), ('REPARADO', 'Reparado')], max_length=9),
        ),
    ]
