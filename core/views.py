from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from .models import *
from formulario.views import *
from urllib.parse import unquote
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from datetime import datetime
from django.shortcuts import render
import locale

from django.shortcuts import render
from django.db import connection
import matplotlib.pyplot as plt
import io
import base64
visitas_departamentosig = 0  # Contador global de visitas

def secpla(request):
    return render(request, "core/secpla.html")

def secpla2(request):
    return render(request, "core/secpla2.html")

def secpla3(request):
    return render(request, "core/secpla3.html")

def inicio(request):
    return render(request,'core/iniciar.html')


def secpla4(request):
    return render(request, "core/secpla4.html")

def secpla5(request):
    return render(request, "core/secpla5.html")


def menu(request):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    ip_address = get_client_ip(request)
    if ip_address:
        user_id = request.COOKIES.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            response = render(request, 'core/home.html', {})
            response.set_cookie('user_id', user_id)
            Visita.objects.create(ip_address=ip_address)
            return response
        else:
            Visita.objects.create(ip_address=ip_address)

    current_page = 'home'
    activities = UserActivity.objects.all()
    solicitud = ProtocoloSolicitud.objects.all()
    data = {
        'usuarios': activities,
        'current_page': current_page,
        'solicitud': solicitud,
    }
    return render(request, 'core/home.html', data)
    
def arcgisregister(request):
    # Obtener el valor de la cookie 'departamento'
    
    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:
        DepartamentoSeleccionado.objects.create(nombre_departamento=departamento_seleccionado)

        
        return redirect('https://experience.arcgis.com/experience/6a6b0cbfb2094d10ba11b439c8060a8d/?return_url=/some_view/')

def arcgisregister1(request):
    # Obtener el valor de la cookie 'departamento'
    departamento_seleccionado = request.COOKIES.get('departamento')

    if departamento_seleccionado:


        user_activity1 = UserActivity1(page='experience.arcgis.com', departamento=departamento_seleccionado)
        user_activity1.save()
        user_activity = UserActivity(page='experience.arcgis.com', departamento=departamento_seleccionado)
        user_activity.save()
        

    # Redirigir al usuario al enlace de ArcGIS
    return redirect('https://experience.arcgis.com/experience/6a6b0cbfb2094d10ba11b439c8060a8d/?return_url=/some_view/')

def geoportalVisita(request):
    departamento_seleccionado = request.COOKIES.get('departamento')
    if departamento_seleccionado:
        DepartamentoSeleccionado.objects.create(nombre_departamento=departamento_seleccionado)

    return redirect('https://geoportal-sig-munivalpo.hub.arcgis.com/')

def gestionsig(request):
    departamento_seleccionado = request.COOKIES.get('departamento')
    if departamento_seleccionado:
        DepartamentoSeleccionado.objects.create(nombre_departamento=departamento_seleccionado)

    return redirect('/Estadistica/')

def SSregistro(request):
    departamento_seleccionado = request.COOKIES.get('departamento')
    if departamento_seleccionado:
        DepartamentoSeleccionado.objects.create(nombre_departamento=departamento_seleccionado)
    return redirect('/solicitud/')


def buscar_protocolo(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        correo_input = request.POST.get("correo_input")  # Podría ser None

        try:
            protocolo = ProtocoloSolicitud.objects.get(codigo=codigo)
            correo_registrado = protocolo.corre_solicitante

            data = {
                "estado": protocolo.estado,
                "correo": correo_registrado,
                "error": False
            }

            # Si se ingresó correo, validar
            if correo_input:
                if correo_input.strip().lower() == correo_registrado.strip().lower():
                    # Coincide: enviar respuesta y archivos
                    respuesta = Respuesta_protocolo.objects.filter(protocolo=protocolo).first()
                    if respuesta:
                        data["respuesta"] = respuesta.respuesta
                        archivos = Archivo_respuesta.objects.filter(respuesta=respuesta)
                        data["archivos"] = [
                            {
                                "url": archivo.archivo.url,
                                "nombre": archivo.archivo.name.split("/")[-1]
                            } for archivo in archivos
                        ]
                    else:
                        data["respuesta"] = None
                        data["archivos"] = []
                else:
                    return JsonResponse({"error": True, "message": "El correo ingresado no coincide con el registrado."})
            # Si no hay correo_input, solo devuelve estado y correo
            return JsonResponse(data)

        except ProtocoloSolicitud.DoesNotExist:
            return JsonResponse({"error": True, "message": "Protocolo no encontrado."})

    return JsonResponse({"error": True, "message": "Método no permitido."})

def obtener_sigla(departamento):

    departamentos = {
    "ALCALDÍA": "ALCALDIA",
    "Dirección de Administración y Finanzas": "DAF",
    "Dirección de Asesoría Jurídica": "DAJ",
    "Dirección desarrollo Económico y Cooperación Internacional": "DES_ECONOMICO",
    "Dirección de Desarrollo Comunitario": "DIDECO",
    "Dirección de Género, Mujeres y Diversidades": "GENERO",
    "Dirección de Medioambiente": "MEDIO AMBIENTE",
    "Dirección de Obras Municipales": "OBRAS MUNICIPALES",
    "Dirección de Operaciones": "OPERACIONES",
    "sin direccion": "Periodo Marcha Blanca",
    "SECPLA": "SECPLA",
    "SIG": "SECPLA",
    "Dirección de Seguridad Ciudadana": "SEGURIDAD",
    "Dirección de Tránsito y Transporte público": "TRANSITO",
    "Dirección de Vivienda, Barrio y Territorio": "VIVIENDA"
    }

    return departamentos.get(departamento, "Departamento no encontrado")


def contar_visita_departamentosig(request):
    global visitas_departamentosig
    visitas_departamentosig += 1
    return JsonResponse({'visitas': visitas_departamentosig})

def obtener_visitas_departamentosig(request):
    return JsonResponse({'visitas': visitas_departamentosig})


def estadisticas(request):
    # Obtener datos de la base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT insumo_id, COUNT(*) FROM formulario_protocolosolicitudinsumo GROUP BY insumo_id")
        resultados = cursor.fetchall()

    insumos = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    # Crear gráfico con Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(insumos, cantidades)
    plt.xlabel('ID de Insumo')
    plt.ylabel('Cantidad de Solicitudes')
    plt.title('Solicitudes por Insumo')

    # Convertir el gráfico a una imagen base64 para mostrar en el HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Pasar datos al template
    contexto = {'imagen': imagen_base64}
    return render(request, 'estadisticas.html', contexto)


# Establecer la configuración regional para formatear números
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

def datos_estadisticas(request):
    numeros_fijos_direcciones = {
        "Alcaldia": 15,
        "Dirección de Desarrollo Comunitario": 270,
        "Dirección de Obras Municipales": 11,
        "Dirección de Tránsito y Transporte público": 9,
        "Dirección de Administración y Finanzas": 38,
        "Dirección desarrollo Económico y Cooperación Internacional": 41,
        "Dirección de Desarrollo Cultural": 11,
        "Dirección de Seguridad Ciudadana": 82,
        "Dirección de Vivienda, Barrio y Territorio": 2,
        "Dirección de Medioambiente": 29,
        "Dirección de Género, Mujeres y Diversidades": 36,
        "Dirección de Operaciones": 31,
        "Dirección de Asesoría Jurídica": 7,
        "SECPLA": 6515,
        "Gabinete": 1,
        "Administración Municipal": 35,
        "Otros": 0
    }

    numeros_fijos_departamento = {
        "Alcaldia": 1735,
        "Dirección de Desarrollo Comunitario": 353,
        "Dirección de Obras Municipales": 282,
        "Dirección de Tránsito y Transporte público": 55,
        "Dirección de Administración y Finanzas": 198,
        "Dirección desarrollo Económico y Cooperación Internacional": 104,
        "Dirección de Desarrollo Cultural": 10,
        "Dirección de Seguridad Ciudadana": 1115,
        "Dirección de Vivienda, Barrio y Territorio": 147,
        "Dirección de Medioambiente": 154,
        "Dirección de Género, Mujeres y Diversidades": 33,
        "Dirección de Asesoría Jurídica": 104,
        "SECPLA": 2218,
        "Gabinete": 1,
        "Administración Municipal": 35,
        "Otros": 0
    }

    numeros_fijos = {
        'archivos': 251,
        'planos_impresos': 295,
        'planos_digitales': 6391,
        'plataformas': 228,
        'productos': 18,
        'total': 0,
        'visitas': 7740,
        'mapa2': 0,
        'soporteweb1':0,
        'soporteweb123':0,
        'promediosoli':0,
        'prome':0


        
    }

    with connection.cursor() as cursor:
        try:
            # Contadores individuales
            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id IN (3, 6, 7, 8) AND ps.estado = 'EJECUTADO'")
            archivos = cursor.fetchone()[0] + numeros_fijos['archivos']

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id = 1 AND ps.estado = 'EJECUTADO'")
            planos_impresos = cursor.fetchone()[0] + numeros_fijos['planos_impresos']

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id = 2 AND ps.estado = 'EJECUTADO'")
            planos_digitales = cursor.fetchone()[0] + numeros_fijos['planos_digitales']

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id IN (4, 10, 11, 9) AND ps.estado = 'EJECUTADO'")
            plataformas = cursor.fetchone()[0] + numeros_fijos['plataformas']

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id IN (12, 13) AND ps.estado = 'EJECUTADO'")
            productos = cursor.fetchone()[0] + numeros_fijos['productos']

            cursor.execute("SELECT COALESCE(COUNT(*), 0) FROM public.core_useractivity WHERE page = 'experience.arcgis.com'")
            mapa2 = cursor.fetchone()[0] + numeros_fijos['mapa2']

            total = archivos + planos_impresos + planos_digitales + plataformas + productos + numeros_fijos['total']

            cursor.execute("SELECT COALESCE(MAX(orden_trabajo::INTEGER), 0) FROM public.formulario_protocolosolicitud;")
            id_mas_alto = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id = 14 AND ps.estado = 'EJECUTADO'")
            soporteweb12 = cursor.fetchone()[0] + numeros_fijos['soporteweb1']

            cursor.execute("SELECT COALESCE(SUM(fpi.cantidad), 0) FROM formulario_protocolosolicitudinsumo fpi JOIN formulario_protocolosolicitud ps ON fpi.protocolosolicitud_id = ps.id WHERE fpi.insumo_id = 15 AND ps.estado = 'EJECUTADO'")
            soporteweb123 = cursor.fetchone()[0] + numeros_fijos['soporteweb123']

            cursor.execute("SELECT ROUND(AVG(cantidad), 2) AS promedio_solicitudes_por_semana FROM ( SELECT DATE_TRUNC('week', fecha)::DATE AS inicio_semana,COUNT(*) AS cantidad FROM formulario_protocolosolicitud GROUP BY inicio_semana) AS solicitudes_por_semana;")
            promedios_de_solicitudes  = cursor.fetchone()[0] + numeros_fijos['promediosoli']

            cursor.execute('''
SELECT AVG(horas_demora) AS promedio_horas_total
FROM (
    SELECT (EXTRACT(EPOCH FROM "fecha_T" - "fecha_L") / (60 * 60)) AS horas_demora
    FROM formulario_protocolosolicitud
    WHERE "fecha_T" IS NOT NULL AND "fecha_L" IS NOT NULL
) AS subconsulta_horas;
''')
            TR  = cursor.fetchone()[0] + numeros_fijos['prome']


            # Datos para el gráfico de direcciones
            cursor.execute("""
                SELECT direccion, COUNT(*)
                FROM formulario_protocolosolicitud
                GROUP BY direccion
            """)
            resultados_direcciones = cursor.fetchall()

            datos_grafico_direcciones = []
            for direccion, cantidad in resultados_direcciones:
                numero_fijo = numeros_fijos_direcciones.get(direccion, 0)
                datos_grafico_direcciones.append({
                    'label': direccion,
                    'cantidad': cantidad + numero_fijo
                })

            cursor.execute("SELECT COALESCE(COUNT(*), 0) FROM core_visita")
            visitas_departamentosig = cursor.fetchone()[0] + numeros_fijos['visitas']

            # Datos para el gráfico general
            datos_grafico = [
                {'label': 'Plataformas', 'cantidad': plataformas},
                {'label': 'Planos Impreso y Digitales', 'cantidad': planos_digitales + planos_impresos},
                {'label': 'Archivos', 'cantidad': archivos},
                {'label': 'Productos', 'cantidad': productos},
            ]

            # Datos para el gráfico de departamentos
            cursor.execute("""
                SELECT nombre, COUNT(*) AS cantidad
                FROM core_departamento
                GROUP BY nombre
            """)

            resultados_departamentos = cursor.fetchall()

            datos_grafico_departamentos = []
            for nombre, cantidad in resultados_departamentos:
                numero_fijo = numeros_fijos_departamento.get(nombre, 0)
                datos_grafico_departamentos.append({
                    'label': nombre,
                    'cantidad': cantidad + numero_fijo
                })

            # Datos para el gráfico semanal (NUEVO CÓDIGO)
            cursor.execute("""
                SELECT
                    DATE_TRUNC('week', fecha)::DATE AS inicio_semana,
                    COUNT(*) AS cantidad
                FROM
                    formulario_protocolosolicitud
                GROUP BY
                    inicio_semana
                ORDER BY
                    inicio_semana
            """)
            resultados_semanales = cursor.fetchall()
            print("Resultados Semanales:", resultados_semanales)  # IMPRESIÓN DE DEPURACIÓN

            labels_semanales = []
            data_semanales = []
            for row in resultados_semanales:
                print("Tipo de row[0]:", type(row[0]))  # IMPRESIÓN DE DEPURACIÓN
                print("Valor de row[0]:", row[0])    # IMPRESIÓN DE DEPURACIÓN
                labels_semanales.append(row[0].strftime('%d/%m/%Y'))
                data_semanales.append(row[1])

            datos_para_grafico_semanal = {
                'labels': labels_semanales,
                'data': data_semanales
            }
            import math
            promedios_de_solicitudes_redondeado = math.ceil(promedios_de_solicitudes)
            # Formatear los números
            archivos_formateado = locale.format_string("%d", archivos, grouping=True)
            planos_impresos_formateado = locale.format_string("%d", planos_impresos, grouping=True)
            planos_digitales_formateado = locale.format_string("%d", planos_digitales, grouping=True)
            plataformas_formateado = locale.format_string("%d", plataformas, grouping=True)
            productos_formateado = locale.format_string("%d", productos, grouping=True)
            total_formateado = locale.format_string("%d", total, grouping=True)
            id_mas_alto_formateado = locale.format_string("%d", id_mas_alto, grouping=True)
            visitas_departamentosig_formateado = locale.format_string("%d", visitas_departamentosig, grouping=True)
            mapa2_formateado = locale.format_string("%d", mapa2, grouping=True)
            soporteweb12_formateado= locale.format_string("%d", soporteweb12, grouping=True)
            soporteweb123_formateado= locale.format_string("%d", soporteweb123, grouping=True)
            promedios_de_solicitudes_formateado = locale.format_string("%d", promedios_de_solicitudes_redondeado, grouping=True)
            TR_formateado = locale.format_string("%.1f", TR, grouping=True)

            return JsonResponse({
                'archivos': archivos_formateado,  # Usar el valor formateado
                'planos_impresos': planos_impresos_formateado,  # Usar el valor formateado
                'planos_digitales': planos_digitales_formateado,  # Usar el valor formateado
                'plataformas': plataformas_formateado,  # Usar el valor formateado
                'productos': productos_formateado,  # Usar el valor formateado
                'id_mas_alto': id_mas_alto_formateado,  # Usar el valor formateado
                'total': total_formateado,  # Usar el valor formateado
                'datos_grafico': datos_grafico,
                'datos_grafico_direcciones': datos_grafico_direcciones,
                'visitas_departamentosig': visitas_departamentosig_formateado,  # Usar el valor formateado
                'datos_grafico_departamentos': datos_grafico_departamentos,
                'mapa2': mapa2_formateado,
                'datos_para_grafico_semanal': datos_para_grafico_semanal,
                'soporteweb12': soporteweb12_formateado,
                'soporteweb123': soporteweb123_formateado,
                'promedios_de_solicitudes': promedios_de_solicitudes_formateado,
                'TR_formateado': TR_formateado,


            })
        except Exception as e:
            print(f"Error en datos_estadisticas: {e}")
            return JsonResponse({'error': str(e)}, status=500)

def guardar_departamento(request):
    if request.method == "POST":
        departamento_nombre = request.POST.get("departamento")
        
        if departamento_nombre:
            # Crear siempre un nuevo departamento, sin importar si ya existe
            departamento = Departamento.objects.create(nombre=departamento_nombre)
            return JsonResponse({"mensaje": "Departamento guardado correctamente", "departamento": departamento.nombre})
        
        return JsonResponse({"error": "No se recibió un departamento"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
