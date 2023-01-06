# DockerDjangoNginx is my project name
# your routing.py file should be in this location where the wsgi.py file is placed
# DockerDjangoNginx/DockerDjangoNginx/routing.py

from .wsgi import *  # add this line to top of your code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import scrumboard.routing as routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})