import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains # Para simular movimientos de ratón
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time # Se usará a través de utils.human_like_delay
import random
import string
import re
import os
import logging
import jsonimport tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

from config import USER_AGENTS, INSTAGRAM_COMMENTS, TIKTOK_COMMENTS, PROXY
from utils import human_like_delay, setup_logging, retry
from temp_mail import generate_realistic_credentials, generate_phone_credentials

# --- Campos globales para login ---
login_username = None
login_password = None

# --- Clases de Bot para mejor organización ---

class InstagramBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def create_account(self, contact_info, full_name, username, password, tm=None):
        """Crea una nueva cuenta de Instagram usando Selenium con email o teléfono."""
        try:
            logging.info("Navegano a la página de registro de Instagram...")
            self.driver.get("https://www.instagram.com/accounts/signup/phone/")
            human_like_delay(2, 4)

            # Verificar que estamos en la página correcta
            current_url = self.driver.current_url
            logging.info(f"URL actual: {current_url}")

            # Determinar si es email o teléfono
            is_email = "@" in contact_info

            # Rellenar email o teléfono
            logging.info(f"Buscando campo de {'email' if is_email else 'teléfono'}...")
            contact_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='emailOrPhone']")))
            logging.info(f"Campo de {'email' if is_email else 'teléfono'} encontrado, rellenando...")
            for char in contact_info:
                contact_field.send_keys(char)
                human_like_delay(0.1, 0.3)
            human_like_delay(1, 2)

            # Rellenar nombre completo
            name_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='fullName']")))
            for char in full_name:
                name_field.send_keys(char)
                human_like_delay(0.1, 0.3)
            human_like_delay(1, 2)

            # Rellenar username
            username_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            for char in username:
                username_field.send_keys(char)
                human_like_delay(0.1, 0.3)
            human_like_delay(1, 2)

            # Rellenar password
            password_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            for char in password:
                password_field.send_keys(char)
                human_like_delay(0.1, 0.3)
            human_like_delay(1, 2)

            # Hacer clic en "Siguiente"
            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Siguiente') or contains(text(), 'Next')]")))
            next_button.click()
            human_like_delay(3, 5)

            # Seleccionar fecha de nacimiento (aleatoria)
            month_select = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Mes:']")))
            month_select.click()
            months = self.driver.find_elements(By.CSS_SELECTOR, "select[title='Mes:'] option")
            random.choice(months).click()
            human_like_delay(1, 2)

            day_select = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Día:']")))
            day_select.click()
            days = self.driver.find_elements(By.CSS_SELECTOR, "select[title='Día:'] option")
            random.choice(days).click()
            human_like_delay(1, 2)

            year_select = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Año:']")))
            year_select.click()
            years = self.driver.find_elements(By.CSS_SELECTOR, "select[title='Año:'] option")
            # Elegir un año entre 1990 y 2005
            valid_years = [y for y in years if 1990 <= int(y.text) <= 2005]
            if valid_years:
                random.choice(valid_years).click()
            human_like_delay(1, 2)

            # Hacer clic en "Siguiente"
            next_button2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Siguiente') or contains(text(), 'Next')]")))
            next_button2.click()
            human_like_delay(3, 5)

            if is_email and tm:
                # Esperar a que aparezca el campo de código de verificación
                code_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email_confirmation_code']")))
                human_like_delay(2, 4)  # Esperar un poco más para que el email llegue

                # Obtener código de verificación del email
                code = tm.get_verification_code("Instagram")
                if not code:
                    logging.error("No se pudo obtener el código de verificación.")
                    return False

                # Ingresar código de verificación
                for char in code:
                    code_field.send_keys(char)
                    human_like_delay(0.2, 0.5)
                human_like_delay(1, 2)
            else:
                # Para teléfono, esperar a que aparezca el campo de código SMS
                code_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='confirmation_code']")))
                human_like_delay(2, 4)

                # Pedir al usuario que ingrese el código SMS
                code = input(f"Ingresa el código de verificación SMS enviado a {contact_info}: ")
                if not code:
                    logging.error("No se proporcionó código de verificación.")
                    return False

                # Ingresar código de verificación
                for char in code:
                    code_field.send_keys(char)
                    human_like_delay(0.2, 0.5)
                human_like_delay(1, 2)

            # Hacer clic en "Siguiente" (botón de registro final)
            logging.info("Buscando botón de registro final...")
            try:
                # Intentar diferentes selectores para el botón de registro
                register_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrarse') or contains(text(), 'Sign up') or contains(text(), 'Crear cuenta')]")))
                logging.info("Botón de registro encontrado, haciendo clic...")
                register_button.click()
                human_like_delay(5, 10)

                # Verificar si la cuenta se creó exitosamente
                try:
                    # Esperar a que aparezca el feed de inicio o el perfil
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Inicio' or @aria-label='Home']")))
                    logging.info(f"Cuenta de Instagram creada exitosamente: {username}")
                    return True
                except TimeoutException:
                    logging.warning("Cuenta creada pero no se pudo verificar el feed de inicio.")
                    return True  # Considerar exitoso si no hay error explícito

            except TimeoutException:
                logging.error("No se pudo encontrar el botón de registro final.")
                return False

            logging.info(f"Cuenta de Instagram creada exitosamente: {username}")
            return True

        except Exception as e:
            logging.error(f"Error creando cuenta de Instagram: {e}")
            return False

    def login(self, username, password):
        """Realiza login en Instagram usando Selenium."""
        try:
            self.driver.get("https://www.instagram.com/")
            human_like_delay(2, 4)

            # Rellenar username
            username_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            for char in username:
                username_field.send_keys(char)
                human_like_delay(0.1, 0.3)

            # Rellenar password
            password_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            for char in password:
                password_field.send_keys(char)
                human_like_delay(0.1, 0.3)

            # Hacer clic en login
            login_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            login_button.click()
            human_like_delay(3, 5)

            # Verificar si login fue exitoso
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Inicio' or @aria-label='Home']")))
                logging.info(f"Login exitoso en Instagram para usuario: {username}")
                return True
            except TimeoutException:
                logging.error("Login fallido: No se pudo verificar la sesión activa.")
                return False

        except Exception as e:
            logging.error(f"Error durante el login en Instagram: {e}")
            return False

    def follow_user(self, user):
        """Sigue a un usuario usando Selenium."""
        try:
            self.driver.get(f"https://www.instagram.com/{user}/")
            human_like_delay(2, 4)

            follow_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Seguir') or contains(text(), 'Follow')]")))
            follow_button.click()
            human_like_delay(1, 2)
            logging.info(f"Usuario '{user}' seguido con éxito.")
        except Exception as e:
            logging.warning(f"Error siguiendo a '{user}': {e}")

    def like_posts(self, user, amount=1):
        """Da like a posts de un usuario usando Selenium."""
        try:
            self.driver.get(f"https://www.instagram.com/{user}/")
            human_like_delay(2, 4)

            # Obtener posts
            posts = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a")))
            for i in range(min(amount, len(posts))):
                post = posts[i]
                post.click()
                human_like_delay(2, 4)

                # Dar like
                like_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Me gusta' or @aria-label='Like']")))
                like_button.click()
                human_like_delay(1, 2)

                # Cerrar post
                close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Cerrar' or @aria-label='Close']")))
                close_button.click()
                human_like_delay(1, 2)

            logging.info(f"Dados {amount} likes a posts de '{user}'.")
        except Exception as e:
            logging.warning(f"Error dando like a posts de '{user}': {e}")

    def like_reels(self, user, amount=1):
        """Da like a reels de un usuario usando Selenium."""
        try:
            self.driver.get(f"https://www.instagram.com/{user}/reels/")
            human_like_delay(2, 4)

            # Obtener reels
            reels = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a")))
            for i in range(min(amount, len(reels))):
                reel = reels[i]
                reel.click()
                human_like_delay(2, 4)

                # Dar like
                like_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Me gusta' or @aria-label='Like']")))
                like_button.click()
                human_like_delay(1, 2)

                # Cerrar reel
                close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Cerrar' or @aria-label='Close']")))
                close_button.click()
                human_like_delay(1, 2)

            logging.info(f"Dados {amount} likes a reels de '{user}'.")
        except Exception as e:
            logging.warning(f"Error dando like a reels de '{user}': {e}")

class TikTokBot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def go_to_user_profile(self, username):
        self.driver.get(f"https://www.tiktok.com/@{username}")

    @retry(attempts=3, delay=3)
    def follow_user(self):
        try:
            # No es necesario el _handle_popups aquí, ya que TikTok es menos propenso.
            follow_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="follow-button"]')))
            self.actions.move_to_element(follow_button).pause(human_like_delay(0.5, 1)).click().perform()
            follow_button.click()
            logging.info(f"Usuario de TikTok '{self.driver.current_url.split('/')[-1]}' seguido con éxito.")
        except (TimeoutException, NoSuchElementException) as e:
            logging.warning(f"Error al intentar seguir en TikTok. Posiblemente ya se sigue al usuario o el botón no se encontró. {e}")
            raise # Re-lanzar para que el decorador retry lo maneje

    @retry(attempts=3, delay=3)
    def _interact_with_single_video(self, video_element, comment=False):
        try:
            video_element.click()
            human_like_delay(2, 4) # Esperar a que el video se abra

            # Intentar dar like
            like_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@data-e2e='video-like-icon' or @data-e2e='video-liked-icon']"))
            )
            # TikTok usa 'video-liked-icon' si ya está dado el like
            if 'video-liked-icon' not in like_button.get_attribute('data-e2e'): # Si no tiene el icono de "liked"
                self.actions.move_to_element(like_button).pause(human_like_delay(0.5, 1)).click().perform()
                logging.info("Like dado en TikTok.")
            else:
                logging.info("El video de TikTok ya tenía like.")
            human_like_delay()

            if comment:
                comment_area = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-e2e="comment-input"]')))
                chosen_comment = random.choice(TIKTOK_COMMENTS)
                for char in chosen_comment:
                    comment_area.send_keys(char) # No usar actions.send_keys aquí, es más directo
                    human_like_delay(0.05, 0.2) # Simular escritura más rápida
                comment_area.send_keys(Keys.RETURN)
                logging.info(f"Comentario '{chosen_comment}' publicado en TikTok.")
            
            human_like_delay(2, 4) # Pausa antes de cerrar el video
            # Cerrar el video (botón de cerrar o tecla ESC)
            try:
                close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@data-e2e='video-close-icon']")))
                close_button.click()
            except TimeoutException:
                self.driver.send_keys(Keys.ESCAPE) # Si no encuentra el botón, intenta con ESC
            logging.info("Video de TikTok cerrado.")

        except (TimeoutException, NoSuchElementException) as e:
            logging.warning(f"Error interactuando con un video de TikTok: {e}")
            raise # Re-lanzar para que el decorador retry lo maneje

    def interact_with_video(self, comment=False, num_videos=1):
        try:
            # Obtener todos los videos visibles
            videos = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-e2e="user-post-item"] a')))
            
            # Interactuar con un número específico de videos
            for i in range(min(num_videos, len(videos))):
                logging.info(f"Interactuando con el video #{i+1} de TikTok.")
                self._interact_with_single_video(videos[i], comment)
                human_like_delay(3, 7) # Pausa entre videos

        except TimeoutException:
            logging.warning("No se encontraron videos para interactuar en TikTok.")
        except (TimeoutException, NoSuchElementException) as e:
            logging.warning(f"Error interactuando con video de TikTok: {e}")

# --- Función para inicializar el WebDriver ---
def setup_driver():
    # Configuración para Chrome móvil vía USB (para servidor, usar headless)
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    opciones = ChromeOptions()
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    opciones.add_experimental_option("mobileEmulation", {"deviceName": "Nexus 5"})  # Simular dispositivo móvil
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    if PROXY:
        opciones.add_argument(f'--proxy-server={PROXY}')
    opciones.add_argument("--headless=new")  # Siempre headless para servidor

    try:
        # Usar chromedriver para móvil
        driver = webdriver.Chrome(options=opciones)
        logging.info("WebDriver de Chrome móvil inicializado con éxito.")
        return driver
    except Exception as e:
        logging.error(f"Error al inicializar el WebDriver de Chrome móvil. Asegúrate de que 'chromedriver.exe' esté en el directorio correcto. Error: {e}")
        return None

# Función para verificar si el bot está logueado en TikTok
def _is_tiktok_logged_in(driver):
    """Verifica si el bot está logueado en TikTok."""
    try:
        wait = WebDriverWait(driver, 10)
        # Buscar un elemento que solo sea visible cuando se está logueado, por ejemplo, el icono de perfil o el botón de subir video
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-e2e='profile-icon'] | //button[@data-e2e='upload-btn']")))
        return True
    except TimeoutException:
        return False

def save_account_to_file(username, password, contact_info):
    """Guarda la cuenta creada en un archivo JSON."""
    try:
        with open('accounts.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"accounts": []}

    account = {
        "username": username,
        "password": password,
        "contact": contact_info
    }
    data["accounts"].append(account)

    with open('accounts.json', 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Cuenta guardada: {username}")

def iniciar_bots(red_social, usuario, cantidad):
    setup_logging() # Configurar el logging al inicio
    logging.info("Iniciando proceso de bots...")

    if not usuario:
        logging.error("Por favor, ingresa el usuario objetivo.")
        return "Error: Por favor, ingresa el usuario objetivo."

    # Cargar cuentas desde accounts.json o crear nuevas si no hay suficientes
    try:
        with open('accounts.json', 'r') as f:
            data = json.load(f)
        accounts = data.get("accounts", [])
    except FileNotFoundError:
        accounts = []

    # Si no hay suficientes cuentas, crear nuevas
    if len(accounts) < cantidad:
        cuentas_a_crear = cantidad - len(accounts)
        logging.info(f"No hay suficientes cuentas. Creando {cuentas_a_crear} nuevas cuentas...")
        for i in range(cuentas_a_crear):
            try:
                # Always use phone for account creation
                contact_info, full_name, username, password = generate_phone_credentials()
                tm = None
                logging.info(f"Generando cuenta #{len(accounts) + i + 1}: {username} con teléfono temporal: {contact_info}")

                # Crear la cuenta nueva usando Selenium
                driver = setup_driver()
                if driver is None:
                    logging.error(f"No se pudo inicializar el driver para crear cuenta #{len(accounts) + i + 1}. Saltando.")
                    continue

                bot = InstagramBot(driver)
                if bot.create_account(contact_info, full_name, username, password, tm):
                    # Guardar la cuenta en el archivo JSON
                    save_account_to_file(username, password, contact_info)
                    accounts.append({"username": username, "password": password, "contact": contact_info})
                    logging.info(f"Cuenta creada y guardada: {username}")
                else:
                    logging.error(f"No se pudo crear la cuenta #{len(accounts) + i + 1}.")

                driver.quit()
                if tm:
                    tm.close()
                human_like_delay(5, 10)  # Pausa entre creaciones de cuentas

            except Exception as e:
                logging.error(f"Error creando cuenta #{len(accounts) + i + 1}: {e}")

    for i in range(cantidad):
        logging.info(f"--- INICIANDO MISIÓN PARA BOT #{i+1} ---")
        try:
            account = accounts[i]
            username = account["username"]
            password = account["password"]

            if red_social == "Instagram":
                driver = setup_driver()
                if driver is None:
                    logging.error(f"No se pudo inicializar el driver para el bot #{i+1}. Saltando esta misión.")
                    continue

                bot = InstagramBot(driver)
                if not bot.login(username, password):
                    logging.error(f"Login fallido para bot #{i+1} con usuario {username}. Saltando.")
                    driver.quit()
                    continue

                # Seguir al usuario objetivo
                bot.follow_user(usuario)

                # Dar like a posts del usuario
                bot.like_posts(usuario, amount=1)

                # Dar like a reels del usuario
                bot.like_reels(usuario, amount=1)

                driver.quit()

            elif red_social == "TikTok":
                driver = setup_driver()
                if driver is None:
                    logging.error(f"No se pudo inicializar el driver para el bot #{i+1}. Saltando esta misión.")
                    continue

                bot = TikTokBot(driver)
                # Para TikTok, necesitarías login con Selenium, pero por ahora solo seguir
                bot.go_to_user_profile(usuario)
                bot.follow_user()
                bot.interact_with_video(comment=False, num_videos=1)
                driver.quit()

        except Exception as e:
            logging.error(f"La misión del bot #{i+1} falló con un error: {e}")
        finally:
            logging.info(f"--- MISIÓN PARA BOT #{i+1} FINALIZADA ---")
            human_like_delay(5, 10)  # Delay entre misiones

    return f"{cantidad} bots finalizados para {red_social}. Cada bot usó una cuenta existente o creó una nueva para seguir, dar like a posts y reels del usuario '{usuario}'. Revisa 'logs/bot_activity.log' para más detalles."

# Configuración de la ventana principal
root = ThemedTk(theme="arc")  # Tema moderno
root.title("Generador Profesional de Bots para Redes Sociales")
root.geometry("600x700")
root.configure(bg="#f0f0f0")

# Frame principal
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Logos
try:
    img_instagram = Image.open("instagram_logo.png")
    img_instagram = img_instagram.resize((50, 50), Image.Resampling.LANCZOS)
    photo_instagram = ImageTk.PhotoImage(img_instagram)
    label_logo_instagram = tk.Label(frame, image=photo_instagram, bg="#f0f0f0")
    label_logo_instagram.pack(side=tk.LEFT, padx=10)
except:
    pass

try:
    img_tiktok = Image.open("tiktok_logo.png")
    img_tiktok = img_tiktok.resize((50, 50), Image.Resampling.LANCZOS)
    photo_tiktok = ImageTk.PhotoImage(img_tiktok)
    label_logo_tiktok = tk.Label(frame, image=photo_tiktok, bg="#f0f0f0")
    label_logo_tiktok.pack(side=tk.RIGHT, padx=10)
except:
    pass

# Selección de red social
var_red_social = tk.StringVar(value="Instagram")
label_red_social = tk.Label(frame, text="Red Social:", bg="#f0f0f0", font=("Arial", 12, "bold"))
label_red_social.pack(pady=10)
combo_red_social = ttk.Combobox(frame, textvariable=var_red_social, values=["Instagram", "TikTok"], state="readonly")
combo_red_social.pack()



# Etiquetas y campos de entrada
label_usuario = tk.Label(frame, text="Usuario Objetivo:", bg="#f0f0f0", font=("Arial", 10))
label_usuario.pack(pady=5)
entry_usuario = tk.Entry(frame, font=("Arial", 10))
entry_usuario.pack()

label_cantidad = tk.Label(frame, text="Cantidad de Bots:", bg="#f0f0f0", font=("Arial", 10))
label_cantidad.pack(pady=5)
entry_cantidad = tk.Entry(frame, font=("Arial", 10))
entry_cantidad.pack()

# Botón para iniciar los bots con animación hover
def start_bots():
    red_social = var_red_social.get()
    usuario = entry_usuario.get()
    try:
        cantidad = int(entry_cantidad.get())
    except ValueError:
        cantidad = 1
    iniciar_bots(red_social, usuario, cantidad)

boton_iniciar = tk.Button(frame, text="Iniciar Bots", command=start_bots, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
boton_iniciar.pack(pady=20)

def on_enter(e):
    boton_iniciar['bg'] = '#45a049'

def on_leave(e):
    boton_iniciar['bg'] = '#4CAF50'

boton_iniciar.bind("<Enter>", on_enter)
boton_iniciar.bind("<Leave>", on_leave)

# Iniciar el bucle principal de la interfaz
root.mainloop()
