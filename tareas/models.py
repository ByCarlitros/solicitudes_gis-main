# from django.db import models

# class Funcionario(models.Model):
#     nombre = models.CharField(max_length=100)
#     apellido = models.CharField(max_length=100)
#     cargo = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.nombre} {self.apellido}"

# class Tarea(models.Model):
#     descripcion = models.TextField()
#     funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
#     fecha_creacion = models.DateField(null=True, blank=True)
#     completada = models.BooleanField(default=False)

#     def __str__(self):
#         return self.descripcion
    



from django.db import models
from django.utils import timezone
from django.utils.timezone import now

class Funcionario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Apoyo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    descripcion = models.CharField(max_length=200)
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(default=now)
    completada = models.BooleanField(default=False) 
    apoyo = models.ManyToManyField('Apoyo', blank=True)
    
    PRIORIDAD_CHOICES = (
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    )
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media',
        help_text="Seleccione la prioridad de la tarea."
    )

    def __str__(self):
        return f"{self.descripcion} ({self.get_prioridad_display()})"
