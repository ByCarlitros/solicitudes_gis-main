import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from control_creacion_usuario.routing import websocket_urlpatterns    # Asegúrate de cambiar "tu_app" por el nombre real de tu app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_control_usuario.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(websocket_urlpatterns),  # Habilitar WebSockets
    }
)
