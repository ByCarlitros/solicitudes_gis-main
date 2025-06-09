from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserActivity(models.Model):
    page = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # Cambiar a DateField o DateTimeField
    departamento = models.CharField(max_length=100)

class Visita(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Visita: {self.fecha_hora}"
class DepartamentoSeleccionado(models.Model):
    nombre_departamento = models.CharField(max_length=255)
    fecha_seleccion = models.DateTimeField(auto_now_add=True)  # Opcional: para guardar la fecha y hora de la selección

    def __str__(self):
        return self.nombre_departamento
    
class Departamento(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class UserActivity1(models.Model):
    page = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # Cambiar a DateField o DateTimeField
    departamento = models.CharField(max_length=100)
