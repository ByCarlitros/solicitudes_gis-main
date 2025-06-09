from django import forms
from .models import Tarea, Funcionario



class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'funcionario', 'fecha_entrega', 'prioridad', 'apoyo']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'apoyo': forms.CheckboxSelectMultiple()  # Usamos CheckboxSelectMultiple para que el usuario seleccione varios apoyos
        }

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nombre', 'apellido', 'cargo']

# # forms.py
# from django import forms
# from .models import Tarea, Funcionario

# class TareaForm(forms.ModelForm):
#     class Meta:
#         model = Tarea
#         fields = ['descripcion', 'funcionario']

# class FuncionarioForm(forms.ModelForm):
#     class Meta:
#         model = Funcionario
#         fields = ['nombre', 'apellido', 'cargo']