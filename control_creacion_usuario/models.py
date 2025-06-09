from django.db import models
import os

def content_file_name_adjunto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % ('adjunto', ext)
    folder = "assets/imagen_sig/" + str(instance.id)# Puedes ajustar la carpeta según tus necesidades
    return os.path.join(folder, filename)


class Imagen_sig(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)

    archivo_adjunto = models.ImageField(upload_to=content_file_name_adjunto, blank=True, null=True)
    
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