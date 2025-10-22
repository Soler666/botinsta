# c:\Users\SOLER DAVID\Desktop\bots\config.py

import os

# --- Configuración del WebDriver ---
EDGE_PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edge_profile")
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")  # Asegúrate de descargar chromedriver.exe compatible con tu versión de Chrome
HEADLESS_MODE = False # Cambiar a True para ejecutar sin interfaz gráfica
MOBILE_MODE = False  # Cambiar a True para ejecutar en móvil vía USB

# --- Configuración de Proxies (Opcional, para un funcionamiento más "real" y escalable) ---
# Ejemplo: "http://user:pass@ip:port" o "socks5://user:pass@ip:port"
PROXY = None # Deja en None si no usas proxy. Si usas, descomenta y configura.

# --- User Agents para simular diferentes navegadores/dispositivos ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0',
    'Mozilla/5.0 (iPad; CPU OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1 EdgA/83.0.4103.88',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', # Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', # Chrome Mac
]

# --- Comentarios para Instagram ---
INSTAGRAM_COMMENTS = ["¡Increíble!", "¡Me gusta mucho!", "¡Fantástico!", "¡Wow!", "¡Gran trabajo!", "Sigue así", "¡Qué buena foto!", "¡Excelente contenido!"]

# --- Comentarios para TikTok ---
TIKTOK_COMMENTS = ["¡Genial video!", "¡Me encanta!", "¡Muy bueno!", "¡Excelente!", "¡Qué crack!", "Para repetir", "¡Súper divertido!", "¡Buen ritmo!"]