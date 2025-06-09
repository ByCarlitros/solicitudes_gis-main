from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio" ),
    path('menu/', views.menu, name="menu"),
    path('arcgis/',views.arcgisregister1,name="arcgis"),
    path('SS/',views.SSregistro,name="SS"),
    path('geoportal/',views.geoportalVisita,name="geoportal"),
    path('buscar_protocolo/',views.buscar_protocolo,name="buscar_protocolo"),
    path('gestionsig/',views.gestionsig,name="gestionsig"),
    path('Estadistica/', views.estadisticas, name='estadisticas'),
    path('datos_estadisticas/', views.datos_estadisticas, name='datos_estadisticas'), 
    path('contar_visita_departamentosig/', views.contar_visita_departamentosig, name='contar_visita_departamentosig'),
    path('obtener_visitas_departamentosig/', views.obtener_visitas_departamentosig, name='obtener_visitas_departamentosig'),
    path('guardar_departamento/', views.guardar_departamento, name='guardar_departamento'),
    path('arcgis1/',views.arcgisregister1,name="arcgis1"),
    path('secpla1/',views.secpla,name="secpla"),
    path('secpla2/',views.secpla2,name="secpla2"),
    path('secpla3/',views.secpla3,name="secpla3"),
    path('secpla4/',views.secpla4,name="secpla4"),
    path('secpla5/',views.secpla5,name="secpla5"),
]
