from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_protocolo, name='crear_protocolo'),
    path('vista_previa/<int:id>', views.vista_previa, name="vista_previa"),     
    path('descargar_pdf/<int:id>', views.descargar_pdf, name="descargar_pdf"),

]