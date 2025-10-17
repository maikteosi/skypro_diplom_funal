import os
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

load_dotenv()


@pytest.fixture(scope="session")  # ← ИЗМЕНИЛИ НА "session"
def driver():
    """Фикстура драйвера для всей сессии тестов"""

    chromedriver_path = r"C:\Users\Михаил\Desktop\skypro_diplom_funal\skypro_diplom_funal\test_project\drivers\chromedriver.exe"
    chrome_binary_path = r"C:\Program Files\Google\Chrome\chrome-win32\chrome.exe"

    if not os.path.exists(chromedriver_path):
        pytest.fail(f"ChromeDriver не найден: {chromedriver_path}")

    if not os.path.exists(chrome_binary_path):
        pytest.fail(f"Тестовый Chrome не найден: {chrome_binary_path}")

    driver_instance = None
    try:
        service = Service(chromedriver_path)

        options = Options()
        options.binary_location = chrome_binary_path

        # Нормальный профиль БЕЗ инкогнито
        test_profile_dir = os.path.join(project_root, "chrome_test_profile")
        options.add_argument(f"--user-data-dir={test_profile_dir}")

        # Обычный User Agent
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0.0.0 Safari/537.36")

        # Базовые опции
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Разрешаем изображения
        prefs = {'profile.default_content_setting_values': {'images': 1}}
        options.add_experimental_option("prefs", prefs)

        print("🚀 ЗАПУСК БРАУЗЕРА ДЛЯ ВСЕХ ТЕСТОВ...")
        driver_instance = webdriver.Chrome(service=service, options=options)

        # Скрываем автоматизацию
        driver_instance.execute_script("Object.defineProperty("
                                       "navigator, 'webdriver', {get: () => undefined})")

        driver_instance.implicitly_wait(10)
        driver_instance.set_page_load_timeout(30)

        print("✅ Браузер запущен для всей сессии тестов!")

        yield driver_instance

        print("🔚 ЗАКРЫТИЕ БРАУЗЕРА ПОСЛЕ ВСЕХ ТЕСТОВ...")
        driver_instance.quit()
        print("✅ Браузер закрыт!")

    except Exception as e:
        if driver_instance:
            driver_instance.quit()
        pytest.fail(f"Не удалось запустить Chrome: {e}")


@pytest.fixture(scope="session")
def api_config():
    return {
        "base_url": os.getenv("API_BASE_URL"),
        "api_key": os.getenv("API_KEY"),
        "headers": {
            "X-API-KEY": os.getenv("API_KEY"),
            "Content-Type": "application/json"
        }
    }
