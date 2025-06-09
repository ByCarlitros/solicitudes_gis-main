from io import BytesIO
from typing_extensions import Buffer
from django.shortcuts import render
from django.http import FileResponse, JsonResponse,HttpResponseBadRequest,HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import date
from .models import *
from .forms import CrearFormulario
import pytz
import uuid
from django.db import transaction

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# CREACION DE PDF.
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,Image
from reportlab.lib.units import inch,mm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import random
import string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from control_creacion_usuario.pdf_generator import *

def generar_codigo():
    caracteres = '0123456789'  # Solo dígitos
    codigo = ''.join(random.choices(caracteres, k=10))
    return codigo


def codigo_es_duplicado(codigo):
    return ProtocoloSolicitud.objects.filter(codigo=codigo).exists()

def crear_protocolo(request):
    if request.method == "POST":
        print("Entrando en el método POST del formulario")
        archivo_adjunto = request.FILES.get('archivo_adjunto', None)
        
        print("Datos POST recibidos:", request.POST)
        print("Insumos recibidos:", request.POST.getlist('insumo'))
        
        try:
            with transaction.atomic():
                Protocolo = ProtocoloSolicitud.objects.create(
                    direccion=request.POST['direccion'],
                    departamento=request.POST['departamento'],
                    nombre_solicitante=request.POST['nombre_solicitante'].title(),
                    nombre_proyecto=request.POST['nombre_proyecto'],
                    corre_solicitante=request.POST['corre_solicitante'],
                    area=request.POST['area'],
                    objetivos=request.POST['objetivos'],
                    cambios_posible=request.POST['cambios_posible'],
                    archivo_adjunto=archivo_adjunto,
                    anexo=request.POST['anexo'],
                )
                archivos_adjuntos = request.FILES.getlist('archivo')
                if archivos_adjuntos:
                    for archivo in archivos_adjuntos:
                        ArchivoProtocolo.objects.create(protocolo=Protocolo, archivo=archivo)


                insumo_ids = [int(insumo.split('_')[1]) for insumo in request.POST.getlist('insumo') if insumo.startswith('insumo_')]
                
                if not insumo_ids:
                    print("No se seleccionaron insumos válidos.")
                    return HttpResponse("No se seleccionaron insumos válidos.", status=400)

                insumos_a_guardar = []
                for insumo_id in insumo_ids:
                    try:
                        insumo = Insumo.objects.get(id=insumo_id)
                        print(f"Insumo encontrado con ID {insumo_id}: {insumo}")
                    except Insumo.DoesNotExist:
                        print(f"Insumo con ID {insumo_id} no encontrado, creando nuevo insumo.")
                        insumo = Insumo.objects.create(id=insumo_id, nombre=f"Insumo {insumo_id}")
                    insumos_a_guardar.append(insumo)

                Protocolo.insumo.set(insumos_a_guardar)

                producto_ids = [int(producto.split('_')[1]) for producto in request.POST.getlist('producto') if producto.startswith('producto_')]
                print("Producto IDs extraídos:", producto_ids)
                
          
           
            data = {'Protocolo': Protocolo}
            nombre_ficha = f"Solicitud{Protocolo.id}_{Protocolo}"
            file_name, status = save_pdf_3(data, nombre_ficha)

            if not status:
                print("Error al generar PDF")
                return HttpResponse("Error al generar PDF", status=500)
            
            archivos_adjuntos = request.FILES.getlist('archivo')
            if archivo_adjunto:
                cuerpo_mensaje = (
                        'Se ha generado una nueva ficha con el código: ' + Protocolo.codigo + 
                        '. Adjunto el archivo PDF correspondiente. Revisa la plataforma de control para ver el archivo correspondiente.'
                    )
            else:
                    cuerpo_mensaje = (
                        'Se ha generado una nueva ficha con el código: ' + Protocolo.codigo + 
                        '. Adjunto el PDF correspondiente.'
                    )

            nombre_archivo = nombre_ficha + ".pdf"

            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)( 
                "solicitudes",
                {"type": "send_update", "message": "actualizar"}
            )

            return FileResponse(open(file_name, 'rb'), content_type='application/pdf', filename=nombre_archivo, as_attachment=True)

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Hubo un error al crear el protocolo: {e}", status=500)

    insumos = Insumo.objects.all()
    return render(request, 'formulario.html', {
        'insumos': insumos,
        'forms': CrearFormulario()
    })
def vista_previa(resquest,id):

    protocolo = ProtocoloSolicitud.objects.get(id=id)
    fecha_actual = protocolo.fecha
    fecha = fecha_actual.strftime('%Y-%m-%d')
    archivos_adjuntos = ArchivoProtocolo.objects.filter(protocolo=protocolo)
    archivos_adjuntos_urls = [archivo.archivo.url for archivo in archivos_adjuntos]

    print(archivos_adjuntos_urls)
    data = {
        'id': protocolo.id,
        'fecha': fecha,
        'nombre_solicitante': protocolo.nombre_solicitante,
        'nombre_proyecto': protocolo.nombre_proyecto,
        'corre_solicitante': protocolo.corre_solicitante,
        'departamento': protocolo.departamento,
        'direccion': protocolo.direccion,
        'area': protocolo.area,
        'objetivos': protocolo.objetivos,
        'insumo': protocolo.insumo,
        'productos': protocolo.producto,
        'Cambios': protocolo.cambios_posible,
        'codigo': protocolo.codigo,
        'archivos_adjuntos_urls': archivos_adjuntos_urls,
    }
    
    return JsonResponse(data)

def descargar_pdf(request,id):
        Protocolo = ProtocoloSolicitud.objects.get(id = id)

        data ={
             'Protocolo':Protocolo,
        }

        nombre_ficha = "Solicitud" + str(Protocolo.id) + "_" + str(Protocolo)

        file_name, status = save_pdf_3(data, nombre_ficha)

        if not status:
            print("----------------")
            print("Error al generar PDF")
            print("----------------")
            return HttpResponse("Error al generar PDF")

        nombre_archivo = nombre_ficha + ".pdf"
        
        return FileResponse(open(file_name, 'rb'), content_type='application/pdf', filename=nombre_archivo, as_attachment=True)
