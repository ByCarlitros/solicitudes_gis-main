from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea, Funcionario
from .forms import TareaForm, FuncionarioForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from django.urls import reverse 
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator





def index(request):
    funcionarios = Funcionario.objects.all()
    # Filtrar las tareas que no están completadas y ordenarlas por id
    tareas = Tarea.objects.filter(completada=False).order_by('-id')

    # Paginación: obtener el número de página desde la solicitud (por defecto es 1)
    page_number = request.GET.get('page', 1)

    # Crear el objeto Paginator, con 10 tareas por página
    paginator = Paginator(tareas, 10)

    # Obtener las tareas de la página solicitada
    page_obj = paginator.get_page(page_number)

    # Enviar las tareas paginadas y otros contextos a la plantilla
    form = TareaForm()
    context = {
        'funcionarios': funcionarios,
        'tareas': page_obj,  # Usar page_obj en lugar de tareas
        'form': form,
    }
    return render(request, 'tareas/index.html', context)

def agregar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TareaForm()
    return render(request, 'tareas/index.html', {'form': form})  # Renderiza index.html siempre

def agregar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FuncionarioForm()
    return render(request, 'tareas/agregar_funcionario.html', {'form': form})

def tareas_por_funcionario(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
    
    # Obtener todas las tareas completadas para ese funcionario
    tareas_list = Tarea.objects.filter(funcionario=funcionario, completada=True).order_by('-id')
    
    # Paginación: muestra 10 tareas por página (puedes ajustar este número según tus necesidades)
    paginator = Paginator(tareas_list, 5)
    
    # Obtener el número de página desde la URL (si no existe, se asigna el valor 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para la plantilla
    context = {
        'tareas': page_obj,
        'funcionario': funcionario,
    }
    
    return render(request, 'tareas/tareas_por_funcionario.html', context)

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .forms import TareaForm
from .models import Tarea

def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    
    if request.method == 'POST':
        # Se intenta obtener 'next' del POST, para saber a dónde redirigir
        next_url = request.POST.get('next', '/')
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            # Redirige a la URL guardada en 'next'
            return HttpResponseRedirect(next_url)
    else:
        # En la solicitud GET, se intenta obtener 'next' de la query string o del HTTP_REFERER
        next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
        form = TareaForm(instance=tarea)
    
    return render(request, 'tareas/editar_tarea.html', {'form': form, 'next_url': next_url})


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()

    # Obtener la URL de referencia para saber de dónde viene el usuario
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)
from .serializers import ApoyoSerializer

def tareas_por_funcionario_json(request, funcionario_id):
    tareas = Tarea.objects.filter(funcionario_id=funcionario_id, completada=False).order_by('-id')

    tareas_list = []
    for tarea in tareas:
        apoyos = ApoyoSerializer(tarea.apoyo.all(), many=True).data  # Serializa los apoyos
        tarea_data = {
            'id': tarea.id,
            'descripcion': tarea.descripcion,
            'funcionario__nombre': tarea.funcionario.nombre,  # Accede al nombre del funcionario
            'fecha_creacion': tarea.fecha_creacion.isoformat(),
            'fecha_entrega': tarea.fecha_entrega.isoformat() if tarea.fecha_entrega else None,
            'prioridad': tarea.prioridad,
            'apoyo': apoyos,  # Agrega los apoyos serializados
            'editar_url': reverse('editar_tarea', args=[tarea.id]),
            'eliminar_url': reverse('eliminar_tarea', args=[tarea.id]),
        }
        tareas_list.append(tarea_data)

    return JsonResponse(tareas_list, safe=False)

class AgregarTareaView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'agregar_tarea.html'  # Nombre de tu template
    success_url = '/lista_tareas/'  # URL a la que se redirige después de crear la tarea

    def form_valid(self, form):
        # Aquí puedes agregar lógica adicional si es necesario, por ejemplo,
        # asignar el usuario que crea la tarea.
        return super().form_valid(form)

from django.shortcuts import redirect, get_object_or_404
from .models import Tarea

from django.shortcuts import get_object_or_404, redirect
from .models import Tarea
from django.contrib import messages

@csrf_exempt
def completar_tarea(request, tarea_id):
    print('x')
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'GET':
        tarea.completada = True
        tarea.save()
        print(f"Tarea {tarea_id} completada: {tarea.completada}")
        messages.success(request, 'Tarea terminada exitosamente.')

    return redirect('tareas_por_funcionario', funcionario_id=tarea.funcionario.id)
    
from rest_framework import generics  # o otro tipo de vista
from .models import Tarea
from .serializers import TareaSerializer

class TareaList(generics.ListAPIView):
    queryset = Tarea.objects.all()  # O la consulta que necesites
    serializer_class = TareaSerializer
