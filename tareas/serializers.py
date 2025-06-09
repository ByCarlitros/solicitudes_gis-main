from rest_framework import serializers
from .models import Tarea, Apoyo  # Importa tus modelos

class ApoyoSerializer(serializers.ModelSerializer):  # Serializador para Apoyo
    class Meta:
        model = Apoyo
        fields = ('id', 'nombre', 'descripcion')  # Incluye los campos que necesites

class TareaSerializer(serializers.ModelSerializer):  # Serializador para Tarea
    apoyo = ApoyoSerializer(many=True, read_only=True)  # Campo para los apoyos

    class Meta:
        model = Tarea
        fields = ('id', 'descripcion', 'funcionario_nombre', 'fecha_creacion', 'fecha_entrega', 'apoyo') # Incluye todos los campos que quieres serializar
        # Opcional: fields = '__all__' si quieres serializar todos los campos del modelo