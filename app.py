import os
import sys
import threading
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.db import models
from django.apps import AppConfig, apps
from django.core.wsgi import get_wsgi_application
from django.core.management.commands.runserver import Command as runserver

# Configuração mínima
BASE_DIR = os.path.dirname(__file__)
settings.configure(
    DEBUG=True,
    SECRET_KEY="chave-secreta",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.admin",
        "django.contrib.auth",
        __name__,
    ],
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
)

# Modelo
class Time(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    fundacao = models.DateField()
    titulos = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

# View
def lista_times(request):
    times = Time.objects.all()
    html = "<h1>Times de Futebol</h1><ul>"
    for t in times:
        html += f"<li>{t.nome} - {t.cidade} (Fundado em {t.fundacao})</li>"
    html += "</ul>"
    return HttpResponse(html)

# URLs
urlpatterns = [
    path("", lista_times),
]

# Registrar app
class InlineAppConfig(AppConfig):
    name = __name__
    verbose_name = "Times"

apps.populate(settings.INSTALLED_APPS)

# Inicializar servidor automaticamente
def start_server():
    sys.argv = ["app.py", "runserver", "0.0.0.0:8000"]
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    # Rodar migrações automaticamente
    execute_from_command_line(["app.py", "migrate"])
    # Iniciar servidor sem precisar digitar nada
    start_server()
