import random
import string
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import human_like_delay
import re

class TempMail:
    def __init__(self):
        self.driver = None
        self.email = None

    def create_temp_email(self):
        """Crea un email temporal usando TempMail."""
        try:
            options = EdgeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Edge(options=options)
            self.driver.get("https://temp-mail.org/")
            human_like_delay(2, 4)

            # Obtener el email generado
            email_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "mail"))
            )
            # Esperar a que el email esté listo (no sea "Loading...")
            max_attempts = 10
            for attempt in range(max_attempts):
                self.email = email_element.get_attribute("value")
                if self.email and "@" in self.email and self.email != "Loading...":
                    print(f"Email temporal creado: {self.email}")
                    return self.email
                human_like_delay(1, 2)
            print("No se pudo obtener un email válido después de varios intentos.")
            return None
        except Exception as e:
            print(f"Error creando email temporal: {e}")
            return None

    def get_verification_code(self, service):
        """Obtiene el código de verificación del email."""
        try:
            # Esperar a que llegue el email
            human_like_delay(10, 15)  # Esperar más tiempo para que llegue el email

            # Buscar el email de verificación
            emails = self.driver.find_elements(By.CSS_SELECTOR, ".inbox-dataList .inbox-dataList-item")
            for email in emails:
                if service.lower() in email.text.lower():
                    email.click()
                    human_like_delay(1, 2)
                    # Extraer el código del cuerpo del email
                    body = self.driver.find_element(By.ID, "mailContent")
                    text = body.text
                    # Buscar un código de 6 dígitos
                    import re
                    code = re.search(r'\b\d{6}\b', text)
                    if code:
                        return code.group(0)
            return None
        except Exception as e:
            print(f"Error obteniendo código de verificación: {e}")
            return None

    def close(self):
        if self.driver:
            self.driver.quit()

def generate_realistic_credentials():
    """Genera credenciales realistas para una cuenta nueva."""
    # Generar nombre completo
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Isabel", "Jose", "Rosa"]
    last_names = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Martin", "Ruiz"]
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    # Generar username con números
    username = f"{full_name.lower().replace(' ', '')}{random.randint(100, 999)}"

    # Generar password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Crear email temporal
    tm = TempMail()
    email = tm.create_temp_email()
    if not email:
        raise Exception("No se pudo crear email temporal")

    return email, full_name, username, password, tm

def generate_phone_credentials():
    """Genera credenciales usando números de teléfono temporales."""
    # Generar nombre completo
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Isabel", "Jose", "Rosa"]
    last_names = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Martin", "Ruiz"]
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    # Generar username con números
    username = f"{full_name.lower().replace(' ', '')}{random.randint(100, 999)}"

    # Generar password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Generar número de teléfono temporal (formato internacional)
    # Usando prefijos de países comunes
    country_codes = ["+1", "+34", "+52", "+57", "+58", "+54", "+56", "+51", "+593", "+595"]
    country_code = random.choice(country_codes)
    phone_number = f"{country_code}{random.randint(100000000, 999999999)}"

    return phone_number, full_name, username, password
