from redis import StrictRedis
from config import REDIS_URL, SECRET_KEY
from itsdangerous import URLSafeTimedSerializer


redis_store = StrictRedis.from_url(REDIS_URL)
external_serializer = URLSafeTimedSerializer(SECRET_KEY)
