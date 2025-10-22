# c:\Users\SOLER DAVID\Desktop\bots\utils.py

import time
import random
import logging
import os
from functools import wraps

# --- Configuración de Logging ---
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "bot_activity.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() # También imprime en consola
        ]
    )

# --- Retrasos con comportamiento humano ---
def human_like_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

# --- Decorador para reintentos ---
def retry(attempts=3, delay=2, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            _attempts = attempts
            _delay = delay
            while _attempts > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logging.warning(f"Intento fallido para {func.__name__}. ({e}). Reintentando en {_delay} segundos...")
                    human_like_delay(_delay, _delay + 1) # Usar human_like_delay para la pausa
                    _attempts -= 1
                    _delay *= backoff
            logging.error(f"La función {func.__name__} falló después de {attempts} intentos.")
            if last_exception:
                raise last_exception # Re-lanzar la última excepción si todos los intentos fallan
        return wrapper
    return decorator