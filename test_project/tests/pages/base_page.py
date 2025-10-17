from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import os


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.base_url = os.getenv("BASE_URL")
        self.wait = WebDriverWait(driver, int(os.getenv("IMPLICIT_WAIT", 10)))

    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """Открыть указанный URL"""
        self.driver.get(url)

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: tuple, timeout: int = None) -> object:
        """Найти элемент на странице"""
        wait = WebDriverWait(self.driver, timeout or int(os.getenv(
            "IMPLICIT_WAIT", 10)))
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Кликнуть на элемент {locator}")
    def click_element(self, locator: tuple) -> None:
        """Кликнуть на элемент"""
        element = self.find_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def enter_text(self, locator: tuple, text: str) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: tuple) -> str:
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """Проверить видимость элемента"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Выбрать значение '{value}' из выпадающего списка {locator}")
    def select_dropdown_by_value(self, locator: tuple, value: str) -> None:
        """Выбрать значение из dropdown по value"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)

    @allure.step("Выбрать текст '{text}' из выпадающего списка {locator}")
    def select_dropdown_by_text(self, locator: tuple, text: str) -> None:
        """Выбрать значение из dropdown по видимому тексту"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    @allure.step("Получить все элементы {locator}")
    def find_elements(self, locator: tuple) -> list:
        """Найти все элементы по локатору"""
        return self.driver.find_elements(*locator)
