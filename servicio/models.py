from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Cars(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plate = models.TextField(null=False)
    model = models.TextField(null=False)
    color = models.TextField(null=False)

    def __str__(self):
            return 'Placa: ' + self.plate
    
class Appointments(models.Model):
    id = models.AutoField(primary_key=True)
    car  = models.ForeignKey(Cars, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    SHIRT_SIZES = [
        ("CANCELAR", "Cancelar"),
        ("PENDIENTE", "Pendiente"),
        ("PROCESO", "Proceso"),
        ("COMPLETADO", "Completado"),
    ]
    state = models.CharField(max_length=10, choices=SHIRT_SIZES)
    observation = models.TextField(null=False)

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    observation = models.TextField(null=False)