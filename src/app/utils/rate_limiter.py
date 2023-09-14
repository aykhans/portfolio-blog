from slowapi import Limiter
from app.utils.custom_functions import get_remote_address

limiter = Limiter(key_func=get_remote_address)