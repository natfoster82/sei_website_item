import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
SEI_URL_BASE = os.environ.get('SEI_URL_BASE', 'https://sei.caveon.com')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')
