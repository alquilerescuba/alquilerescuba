from decouple import config
import os
from pathlib import Path
import sys
import dj_database_url
import boto3
from botocore.client import Config

BASE_DIR = Path(__file__).resolve().parent.parent

# ========== CARGAR VARIABLES DE ENTORNO ==========
if not os.environ.get("AWS_ACCESS_KEY_ID"):
    os.environ["AWS_ACCESS_KEY_ID"] = config("AWS_ACCESS_KEY_ID", default="")
    os.environ["AWS_SECRET_ACCESS_KEY"] = config("AWS_SECRET_ACCESS_KEY", default="")
    os.environ["AWS_STORAGE_BUCKET_NAME"] = config(
        "AWS_STORAGE_BUCKET_NAME", default="dea4ever-images"
    )
    os.environ["AWS_S3_ENDPOINT_URL"] = config("AWS_S3_ENDPOINT_URL", default="")
    os.environ["AWS_S3_CUSTOM_DOMAIN"] = config(
        "AWS_S3_CUSTOM_DOMAIN", default="pub-1fe93bd268f646bf9c370e43aad1ed3b.r2.dev"
    )

SECRET_KEY = "django-insecure-tu-clave-secreta-aqui"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "dea4ever.pythonanywhere.com"]

# ========== APLICACIONES ==========
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "storages",
    "core",
    "properties",
    "leads",
    "accounts",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ========== BASE DE DATOS ==========
if "RENDER" in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = [".onrender.com"]
    DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ========== ARCHIVOS ESTÁTICOS ==========
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ========== ARCHIVOS MEDIA (CLOUDFLARE R2) ==========
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "dea4ever-images")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = "auto"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

AWS_S3_CUSTOM_DOMAIN = os.environ.get(
    "AWS_S3_CUSTOM_DOMAIN", "pub-1fe93bd268f646bf9c370e43aad1ed3b.r2.dev"
)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

print(f"🔧 Usando R2: {MEDIA_URL}")

# ========== VERIFICACIÓN DE CONEXIÓN A R2 ==========
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=AWS_S3_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )
        s3_client.put_object(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key="test.txt",
            Body=b"Test content",
            ACL="public-read",
        )
        print(
            f"✅ Conexión a R2 exitosa. Archivo test.txt subido a {AWS_STORAGE_BUCKET_NAME}"
        )
    except Exception as e:
        print(f"❌ Error conectando a R2: {e}")

# ========== OTRAS CONFIGURACIONES ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Havana"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
BUSINESS_WHATSAPP = "+5354026428"

print("✅ Configuración cargada correctamente")
