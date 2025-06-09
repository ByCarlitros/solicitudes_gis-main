import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,Image
from reportlab.lib.units import inch
from formulario.models import ProtocoloSolicitud
from io import BytesIO
from django.http import HttpResponse
import uuid
from datetime import datetime
from io import BytesIO, StringIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings


def Generar_PDF(id):
        Protocolo = ProtocoloSolicitud.objects.get(id = id)
        Protocolo.codigo = str(Protocolo.id)
        # Crear un buffer de memoria para el PDF
        buffer = BytesIO()
        # Crear un objeto de tipo SimpleDocTemplate con el buffer y el tamaño de página deseado (en este caso, carta)
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # # Crear una lista con los elementos que se agregarán al PDF
        elementos = []
        logo = Image('media/assets/image/logosig.png', width=120, height=60)
        # Agregar el espacio a la lista de elementos
        tabla = Table([['', logo, "                                      N° Orden de Trabajo:\n                                      (Uso Interno SIG)", "                           "]])
        # Agregar estilos a la tabla
        tabla.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                                    ('LEFTPADDING', (1, 0), (1, -1), -60),
                                    ('TOPPADDING', (0, 0), (-1, -1), -22),
                                    ('BOTTOMPADDING', (0, 0), (-1, -1), -10),
                                    ('INNERGRID', (3, 0), (3, 0), 0.25, colors.black),
                                    ('BOX', (3, 0), (3, 1), 0.25, colors.black),
                                    ('ROWSPAN', (0, 0), (0, 1), 2),
                                    ]))
                                    
        elementos.append(tabla)
        # Agregar un logo al PDF
       
        elementos.append(Spacer(1, 0.1 * inch))
        # Agregar un título al PDF
        estilo_titulo = getSampleStyleSheet()["Title"]
        titulo = Paragraph("Protocolo Traspaso Datos Geoespaciales", estilo_titulo)
        
        # Crear un espacio horizontal entre el logo y el título
        
        tabla = Table([[titulo]])
        
        tabla.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))

        # Agregar los datos de la solicitud al PDF
        
        elementos.append(tabla)

        elementos.append(Spacer(1, 0.1 * inch))
        
        estilo_parrafo = ParagraphStyle(name='Normal', fontSize=8, leading=10)
        # Obtener una instancia de los estilos de párrafo de muestra
        sample_styles = getSampleStyleSheet()

        # Crear un nuevo estilo de párrafo para el texto del código
        codigo_style = sample_styles["Normal"]
        codigo_style.fontSize = 20  # Tamaño de fuente diferente
        codigo_style.leading = 56  # Interlineado diferente

        # Crear el párrafo para el texto del código con el nuevo estilo
        texto_codigo = Protocolo.codigo
        # Crear el texto completo del subtitulo con el texto del código
        subtitulo_texto = "Para revisar su estado debe ir a gestion de tiempo, su código es <b>" + texto_codigo + "</b>"

        # Crear el párrafo con el texto completo y el estilo del subtitulo
        subtitulo = Paragraph(subtitulo_texto, estilo_parrafo)

        # Agregar el párrafo al elemento
        elementos.append(subtitulo)

        # Agregar un espacio vertical despu1és del párrafo del código
        elementos.append(Spacer(1, 0.1 * inch))
        
        # Crear un estilo de párrafo
        
        # Dividir el texto en varias líneas
        texto_objetivos = Protocolo.objetivos
        texto_direccion = Protocolo.direccion
        texto_despartamento = Protocolo.departamento
        texto_proyecto = Protocolo.nombre_proyecto
        texto_nombre = Protocolo.nombre_solicitante
        texto_corre_solicitante = Protocolo.corre_solicitante
        texto_area = Protocolo.area
        texto_insumo = Protocolo.insumo
        texto_producto = Protocolo.producto
        texto_cambio = Protocolo.cambios_posible

        parrafo_despartamento = Paragraph(texto_despartamento, estilo_parrafo, bulletText='')
        parrafo_direccion = Paragraph(texto_direccion, estilo_parrafo, bulletText='')
        parrafo_objetivos = Paragraph(texto_objetivos, estilo_parrafo, bulletText='')
        parrafo_proyecto = Paragraph(texto_proyecto, estilo_parrafo, bulletText='')
        parrafo_nombre = Paragraph(texto_nombre, estilo_parrafo, bulletText='')
        parrafo_correo = Paragraph(texto_corre_solicitante, estilo_parrafo, bulletText='')
        parrafo_area = Paragraph(texto_area, estilo_parrafo, bulletText='')
        parrafo_insumo = Paragraph(texto_insumo, estilo_parrafo, bulletText='')
        parrafo_producto = Paragraph(texto_producto, estilo_parrafo, bulletText='')
        parrafo_cambio = Paragraph(texto_cambio, estilo_parrafo, bulletText='')


        fecha_actual = Protocolo.fecha
        # Obtener solo la fecha (año, mes, día)
        fecha = fecha_actual.strftime('%Y-%m-%d')

        # Crear una tabla con los datos de la solicitud
        datos = [
            ["Fecha de la solicitud", fecha],
            ["Direccion", parrafo_direccion],
            ["Departamento o Unidad Responsable", parrafo_despartamento],
            ["Nombre del solicitante", parrafo_nombre],
            ["Nombre del proyecto", parrafo_proyecto],
            ["Correo del solicitante",parrafo_correo],
            ["Área de estudio o intervencion (Cerro,Sector,UV,etc.)", parrafo_area],
            ["Objetivos de las solicitud ", parrafo_objetivos],
            ["Insumo solicitado y formato (KMZ, SHAPE, CAD, EXCEL,\n DESARROLLO ARCGIS ONLINE)\n"+
            "(Formulario Digital, cuadro de mando, Planos Digitales,\n Planos Impresos,  Aplicacion web y otra\n herramientas territoriales.) (previa a la Reunion)\n"
            + "Para los archivos KMZ, SHAPE y CAD\n sólo se puede entregar la información \nde una porción del territorio."
             , parrafo_insumo],
            ["Producto (ESTUDIO, INFORME, TABLA, PLANO\nU OTROSQUE DERIVIRAN DE LA \nINFORMACION ENTREGADA.)", parrafo_producto],
            ["Posibles cambios en el Insumo Entregado  ", parrafo_cambio]
        ]
        tabla = Table(datos,colWidths=[letter[0]*0.9/2]*2)
        # Aplicar un estilo a la tabla
        estilo_tabla = TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
        # Agregar más elementos al PDF según sea necesario
        tabla.setStyle(estilo_tabla)
        elementos.append(tabla)
        # Agregar más elementos al PDF según sea necesario
        
        tabla2 = Table([["V° B°\n Jefatura Directa", "V° B°\nDepartamento SIG"]],colWidths=[letter[0]*0.9/2]*2)
        tabla2.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 43),
        ]))
        elementos.append(tabla2)

        # Construir el PDF y enviarlo como respuesta al usuario
        doc.build(elementos)

        
        return buffer

def save_pdf_3(params, filename):
    template = get_template('pdf_protocolo.html')
    html = template.render(params)
    # file_name = str(uuid.uuid4())
    file_name = filename
    output_filename = str(settings.BASE_DIR) + '/media/' + str(file_name) + '.pdf'
    
    try: 
        resultFile = open(output_filename, "w+b")

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(html, dest=resultFile, encoding='utf-8', show_error_as_pdf=True, debug=True)

        print("ººººººººººººººººº")
        print(pisaStatus.error("Error"))
        print("ººººººººººººººººº")

        # close output file
        resultFile.close()
    except Exception as e:
        print("-------------------")
        print(e)
        print("-------------------")

    return output_filename, pisaStatus.error