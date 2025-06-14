from django.db import models
import os
from django.contrib.auth.models import User

def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('adjunto', ext)
    folder = "assets/imagen_sig/" + str(instance.id)# Puedes ajustar la carpeta según tus necesidades
    return os.path.join(folder, filename)




class Imagen_sig(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    archivo_adjunto = models.ImageField(upload_to=content_file_name_adjunto, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)# NUEVO CAMPO

    class Meta:
        verbose_name = "Imagen_sig"
        verbose_name_plural = "Imagenes_sig"


def content_file_name_adjunto_pdf(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('adjunto', ext)
    folder = "assets/pdf_sig/" + str(instance.id)# Puedes ajustar la carpeta según tus necesidades
    return os.path.join(folder, filename)

class PDF_sig(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    archivo_adjunto = models.FileField(upload_to=content_file_name_adjunto_pdf, blank=True, null=True)
    nombre = models.TextField()
    class Meta:
        verbose_name = "pdf_sig"
        verbose_name_plural = "pdfs_sig"

from datetime import datetime
class Solicitud(models.Model):
    ESTADO_CHOICES = [
        (1, 'En revisión'),
        (2, 'Aprobado'),
        (3, 'Rechazado'),
    ]

    nombre_usuario = models.CharField(max_length=255)
    nombre_archivo = models.CharField(max_length=255)
    validado_por = models.CharField(max_length=255, default="Ninguno")
    fecha_subida = models.DateTimeField(default=datetime.now)  # Cambié a DateTimeField
    fecha_actualizacion = models.DateTimeField()  # Cambié a DateTimeField
    fuente = models.CharField(max_length=255)
    lugar = models.CharField(max_length=255)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=1)
    comentario = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'solicitud'

    def __str__(self):
        return self.nombre_archivo