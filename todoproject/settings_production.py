import os
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['vincentmugondora.pythonanywhere.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
STATIC_ROOT = '/home/vincentmugondora/mysite/static'
