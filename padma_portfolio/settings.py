"""
Django settings for padma_portfolio project.
Ready for local development + Render deployment + Cloudinary media storage + Brevo SMTP email.
"""

import os
from pathlib import Path
from urllib.parse import urlparse, unquote

import dj_database_url


# =========================================================
# BASE DIRECTORY
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY SETTINGS
# =========================================================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key-change-this"
)

DEBUG = os.environ.get(
    "DEBUG",
    "False" if os.environ.get("RENDER_EXTERNAL_HOSTNAME") else "True"
).lower() == "true"


# =========================================================
# ALLOWED HOSTS
# =========================================================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

EXTRA_ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "")

if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS += [
        host.strip()
        for host in EXTRA_ALLOWED_HOSTS.split(",")
        if host.strip()
    ]


# =========================================================
# CSRF SETTINGS
# =========================================================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.onrender.com",
]

EXTRA_CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "")

if EXTRA_CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS += [
        origin.strip()
        for origin in EXTRA_CSRF_TRUSTED_ORIGINS.split(",")
        if origin.strip()
    ]

if RENDER_EXTERNAL_HOSTNAME:
    render_origin = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)


# =========================================================
# APPLICATIONS
# =========================================================
INSTALLED_APPS = [
    # Cloudinary
    # Do NOT add "cloudinary_storage" here because it can break collectstatic on Render.
    "cloudinary",

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Custom app
    "portfolio",
]


# =========================================================
# MIDDLEWARE
# =========================================================
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


# =========================================================
# URLS / WSGI
# =========================================================
ROOT_URLCONF = "padma_portfolio.urls"
WSGI_APPLICATION = "padma_portfolio.wsgi.application"


# =========================================================
# TEMPLATES
# =========================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# DATABASE
# =========================================================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================================================
# LANGUAGE AND TIME
# =========================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kuala_Lumpur"
USE_I18N = True
USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = []

if (BASE_DIR / "static").exists():
    STATICFILES_DIRS.append(BASE_DIR / "static")

# WhiteNoise handles CSS, JS, and static images
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================================================
# MEDIA FILES / CLOUDINARY
# =========================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "")

USE_CLOUDINARY = os.environ.get(
    "USE_CLOUDINARY",
    "True" if CLOUDINARY_URL or os.environ.get("CLOUDINARY_CLOUD_NAME") else "False"
).lower() == "true"

# Option 1 for Render:
# CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
#
# Option 2:
# CLOUDINARY_CLOUD_NAME=your_cloud_name
# CLOUDINARY_API_KEY=your_api_key
# CLOUDINARY_API_SECRET=your_api_secret

if CLOUDINARY_URL:
    parsed_cloudinary_url = urlparse(CLOUDINARY_URL)

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": parsed_cloudinary_url.hostname or "",
        "API_KEY": unquote(parsed_cloudinary_url.username or ""),
        "API_SECRET": unquote(parsed_cloudinary_url.password or ""),
    }
else:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY", ""),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET", ""),
    }


# =========================================================
# DJANGO 6 STORAGE SETTINGS
# =========================================================
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USE_CLOUDINARY
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Compatibility setting for django-cloudinary-storage
if USE_CLOUDINARY:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# =========================================================
# EMAIL SETTINGS - BREVO SMTP
# =========================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp-relay.brevo.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER
)

CONTACT_RECEIVER_EMAIL = os.environ.get(
    "CONTACT_RECEIVER_EMAIL",
    "padmavathyprasanna4@gmail.com"
)


# =========================================================
# LOGIN / LOGOUT
# =========================================================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"


# =========================================================
# SECURITY SETTINGS FOR RENDER PRODUCTION
# =========================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =========================================================
# DEFAULT PRIMARY KEY FIELD
# =========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
