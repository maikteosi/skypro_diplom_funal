from .base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class SearchPage(BasePage):
    """Класс для работы со страницей поиска и расширенного поиска"""

    # Локаторы для расширенного поиска
    FILM_NAME_INPUT = (By.CSS_SELECTOR, "input[name='film_name']")
    YEAR_INPUT = (By.CSS_SELECTOR, "input[name='year']")
    COUNTRY_SELECT = (By.CSS_SELECTOR, "select[name='country']")
    GENRE_SELECT = (By.CSS_SELECTOR, "select[name='genre']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search_results .item")

    # Локаторы для поиска по жанрам
    GENRES_FILTER = (By.XPATH, "//a[contains(text(), 'Жанры')]")
    FANTASY_GENRE = (By.XPATH, "//a[contains(text(), 'фантастика')"
                               " or contains(text(), 'Фантастика')]")
    BEST_20_FILMS = (By.XPATH, "//a[contains(text(), 'лучшие 20')"
                               " or contains(text(), 'Лучшие 20')]")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name='sort']")
    SORT_BY_RATING = (By.XPATH, "//option[contains(text(), 'рейтингу')]")
    SORT_BY_NAME = (By.XPATH, "//option[contains(text(), 'названию')]")

    # Локаторы для результатов поиска
    FILM_ITEM = (By.CSS_SELECTOR, ".film-item, .movie-item")
    FAVORITE_ICON = (By.CSS_SELECTOR, ".favorite-icon, .bookmark-icon")
    THREE_DOTS_MENU = (By.CSS_SELECTOR, ".context-menu, .dropdown-toggle")
    ADD_TO_FAVORITES = (By.XPATH, "//a[contains(text(), 'Любимые фильмы')]")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Заполнить поле названия фильма: '{film_name}'")
    def enter_film_name(self, film_name: str) -> None:
        """Ввести название фильма в поле поиска"""
        self.enter_text(self.FILM_NAME_INPUT, film_name)

    @allure.step("Заполнить поле года: '{year}'")
    def enter_year(self, year: str) -> None:
        """Ввести год выпуска фильма"""
        self.enter_text(self.YEAR_INPUT, year)

    @allure.step("Выбрать страну: '{country}'")
    def select_country(self, country: str) -> None:
        """Выбрать страну производства из выпадающего списка"""
        # Реализация выбора из dropdown
        country_option = (By.XPATH, f"//option[contains(text(), '{country}')]")
        self.click_element(country_option)

    @allure.step("Выполнить поиск")
    def perform_search(self) -> None:
        """Нажать кнопку поиска"""
        self.click_element(self.SEARCH_BUTTON)

    @allure.step("Выбрать жанр 'Фантастика'")
    def select_fantasy_genre(self) -> None:
        """Выбрать жанр фантастика"""
        self.click_element(self.FANTASY_GENRE)

    @allure.step("Открыть категорию 'Лучшие 20 фильмов'")
    def open_best_20_films(self) -> None:
        """Открыть список лучших 20 фильмов"""
        self.click_element(self.BEST_20_FILMS)

    @allure.step("Выбрать сортировку по рейтингу")
    def sort_by_rating(self) -> None:
        """Выбрать сортировку по рейтингу"""
        self.click_element(self.SORT_DROPDOWN)
        self.click_element(self.SORT_BY_RATING)

    @allure.step("Выбрать сортировку по названию")
    def sort_by_name(self) -> None:
        """Выбрать сортировку по названию"""
        self.click_element(self.SORT_DROPDOWN)
        self.click_element(self.SORT_BY_NAME)

    @allure.step("Открыть меню трех точек для фильма")
    def open_film_context_menu(self, film_index: int = 0) -> None:
        """
        Открыть контекстное меню для фильма

        Args:
            film_index: Индекс фильма в списке (по умолчанию 0 - первый)
        """
        film_elements = self.driver.find_elements(*self.THREE_DOTS_MENU)
        if film_elements and len(film_elements) > film_index:
            film_elements[film_index].click()

    @allure.step("Добавить фильм в любимые через контекстное меню")
    def add_to_favorites_via_menu(self) -> None:
        """Добавить фильм в любимые через контекстное меню"""
        self.click_element(self.ADD_TO_FAVORITES)

    @allure.step("Получить количество результатов поиска")
    def get_search_results_count(self) -> int:
        """Получить количество найденных фильмов"""
        results = self.driver.find_elements(*self.SEARCH_RESULTS)
        return len(results)

    @allure.step("Проверить наличие результатов поиска")
    def has_search_results(self) -> bool:
        """Проверить, есть ли результаты поиска"""
        return self.get_search_results_count() > 0

    @allure.step("Выбрать жанры из фильтра")
    def select_genre_filter(self) -> None:
        """Выбрать фильтр по жанрам"""
        self.click_element(self.GENRES_FILTER)
