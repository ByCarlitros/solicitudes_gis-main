from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar_tarea/', views.agregar_tarea, name='agregar_tarea'),
    path('agregar_funcionario/', views.agregar_funcionario, name='agregar_funcionario'),
    path('tareas_por_funcionario/<int:funcionario_id>/', views.tareas_por_funcionario, name='tareas_por_funcionario'),
    path('eliminar_tarea/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('completar_tarea/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
    path('api/tareas_por_funcionario/<int:funcionario_id>/', views.tareas_por_funcionario_json, name='tareas_por_funcionario_json'),

    # Modal edición
    path('ajax/editar-tarea/<int:tarea_id>/', views.cargar_formulario_editar_tarea, name='ajax_editar_tarea'),
    path('ajax/guardar-edicion-tarea/<int:tarea_id>/', views.editar_tarea, name='guardar_edicion_tarea'),
]