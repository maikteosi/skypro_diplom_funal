from .base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class MainPage(BasePage):
    """Класс для работы с главной страницей Кинопоиска"""

    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='kp_query']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ADVANCED_SEARCH_BUTTON = (By.XPATH, "//a[contains(text(), "
                                        "'расширенный поиск')]")
    MOVIES_MENU = (By.XPATH, "//a[contains(text(), 'Фильмы')]")
    SERIES_MENU = (By.XPATH, "//a[contains(text(), 'Сериалы')]")
    FAVORITE_BUTTON = (By.CSS_SELECTOR, "[data-test-id='favorite-button']")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> None:
        """Открыть главную страницу"""
        self.open(self.base_url)

    @allure.step("Выполнить поиск фильма '{film_name}'")
    def search_film(self, film_name: str) -> None:
        """Выполнить поиск фильма"""
        self.enter_text(self.SEARCH_INPUT, film_name)
        self.click_element(self.SEARCH_BUTTON)

    @allure.step("Открыть расширенный поиск")
    def open_advanced_search(self) -> None:
        """Открыть расширенный поиск"""
        self.click_element(self.ADVANCED_SEARCH_BUTTON)

    @allure.step("Перейти в раздел 'Фильмы'")
    def go_to_movies_section(self) -> None:
        """Перейти в раздел фильмов"""
        self.click_element(self.MOVIES_MENU)

    @allure.step("Добавить фильм в избранное")
    def add_to_favorite(self) -> None:
        """Добавить фильм в избранное"""
        self.click_element(self.FAVORITE_BUTTON)
