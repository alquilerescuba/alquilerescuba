import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Datos del superusuario
username = "admin"
email = "admin@ejemplo.com"
password = "Admin123456"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superusuario "{username}" creado exitosamente')
else:
    print(f'ℹ️ El superusuario "{username}" ya existe')
