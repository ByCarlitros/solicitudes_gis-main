from django.urls import re_path
from .consumers import SolicitudConsumer  # Importa tu WebSocket Consumer

websocket_urlpatterns = [
    re_path(r"ws/solicitudes/$", SolicitudConsumer.as_asgi()),  # Ruta WebSocket
]
