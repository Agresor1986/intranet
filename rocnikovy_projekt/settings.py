import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


SECRET_KEY = 'django-insecure-0*x0y@lapyl2+5-l4b05gq^1auag-27r$#2kfxw2kuy4f&vt8('

DEBUG = True

ALLOWED_HOSTS = ['www.firma-intranet.great-site.net', 'intranet-tlij.onrender.com', 'localhost', '127.0.0.1']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'chat',
    'cal',
    'forum',
    'polls',
    'documents',
    'mail',
    'notifications',
    'rocnikovy_projekt',
    'channels',
    'daphne' ,
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rocnikovy_projekt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rocnikovy_projekt.wsgi.application'
ASGI_APPLICATION = 'rocnikovy_projekt.asgi.application'



DATABASES = {
    'default': dj_database_url.config(default='postgresql://intranet_databaza_l76w_user:2UVDStnxRxq5C2NijV747B0Cm1eQiZvF@dpg-d159bb3uibrs73bnmg2g-a.frankfurt-postgres.render.com/intranet_databaza_l76w')
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'sk'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  
DEFAULT_FROM_EMAIL = 'stredak.michael@gmail.com'

BASE_URL = "https://www.firma-intranet.great-site.net"

SESSION_COOKIE_AGE = 900  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  

CSRF_COOKIE_SECURE = True 

CSRF_TRUSTED_ORIGINS = [
    'https://www.firma-intranet.great-site.net', 
]

SECURE_BROWSER_XSS_FILTER = True   
SECURE_CONTENT_TYPE_NOSNIFF = True  
X_FRAME_OPTIONS = 'DENY' 
SESSION_COOKIE_HTTPONLY = True  

SESSION_COOKIE_SECURE = True  
