import pytest
import requests
import allure
from typing import Dict, Any


@allure.epic("Kinopoisk API Tests")
@allure.feature("API тесты для Кинопоиска")
class TestKinopoiskAPI:
    """Класс для API тестов Кинопоиска"""

    @allure.story("Позитивные тесты API")
    @allure.title("Поиск фильмов по ключевому слову 'миньоны'")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_search_films_by_keyword(self, api_config: Dict[str, Any]) -> None:
        """
        Тест поиска фильмов по ключевому слову

        Args:
            api_config: Конфигурация API с базовым URL и заголовками
        """
        with allure.step("Отправить GET запрос для поиска по ключевому слову"):
            url = f"{api_config['base_url']}/api/v2.1/films/search-by-keyword"
            params = {"keyword": "миньоны"}

            response = requests.get(
                url,
                headers=api_config["headers"],
                params=params
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, (f"Ожидался статус 200, "
                                                 f"получен {response.status_code}")

        with allure.step("Проверить время ответа"):
            assert response.elapsed.total_seconds() < 1.1, "Время ответа превышает 1.1 секунды"

        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert "films" in response_data, "В ответе отсутствует ключ 'films'"
            assert len(response_data["films"]) > 0, "Список фильмов пуст"

            film = response_data["films"][0]
            assert "filmId" in film, "В фильме отсутствует ID"
            assert "nameRu" in film or "nameEn" in film, "В фильме отсутствует название"

    @allure.story("Позитивные тесты API")
    @allure.title("Поиск фильмов по различным фильтрам")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_search_films_with_filters(self, api_config: Dict[str, Any]) -> None:
        """
        Тест поиска фильмов с применением фильтров

        Args:
            api_config: Конфигурация API с базовым URL и заголовками
        """
        with allure.step("Отправить GET запрос с фильтрами"):
            url = f"{api_config['base_url']}/api/v2.2/films"
            params = {
                "countries": 1,
                "genres": 11,
                "order": "RATING",
                "type": "FILM",
                "ratingFrom": 7,
                "ratingTo": 10,
                "yearFrom": 2020,
                "yearTo": 2020,
                "page": 1
            }

            response = requests.get(
                url,
                headers=api_config["headers"],
                params=params
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, f"ОР 200, получен {response.status_code}"

        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert "items" in response_data, "В ответе отсутствует ключ 'items'"
            assert len(response_data["items"]) > 0, "Список фильмов пуст"

            film = response_data["items"][0]
            assert "kinopoiskId" in film, "В фильме отсутствует kinopoiskId"
            assert "genres" in film, "В фильме отсутствует информация о жанрах"
            assert "countries" in film, "В фильме отсутствует информация о странах"

    @allure.story("Позитивные тесты API")
    @allure.title("Получение топ-250 фильмов")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_top_250_films(self, api_config: Dict[str, Any]) -> None:
        """
        Тест получения топ-250 фильмов

        Args:
            api_config: Конфигурация API с базовым URL и заголовками
        """
        with allure.step("Отправить GET запрос для получения топ-250"):
            url = f"{api_config['base_url']}/api/v2.2/films/top"
            params = {
                "type": "TOP_250_BEST_FILMS",
                "page": 1
            }

            response = requests.get(
                url,
                headers=api_config["headers"],
                params=params
            )

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, f"ОР 200, получен {response.status_code}"

        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert "films" in response_data, "В ответе отсутствует ключ 'films'"
            assert len(response_data["films"]) > 0, "Список фильмов пуст"

            film = response_data["films"][0]
            assert "filmId" in film, "В фильме отсутствует filmId"
            assert "rating" in film, "В фильме отсутствует рейтинг"

    @allure.story("Негативные тесты API")
    @allure.title("Запрос без API-ключа")
    @pytest.mark.api
    @pytest.mark.regression
    def test_request_without_api_key(self, api_config: Dict[str, Any]) -> None:
        """
        Тест запроса без API ключа

        Args:
            api_config: Конфигурация API с базовым URL и заголовками
        """
        with allure.step("Отправить GET запрос без API ключа"):
            url = f"{api_config['base_url']}/api/v2.2/films/252002"

            response = requests.get(url)

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401, f"ОР 401, получен {response.status_code}"

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert "message" in response_data, "В ответе отсутствует сообщение об ошибке"

    @allure.story("Негативные тесты API")
    @allure.title("Запрос несуществующего фильма")
    @pytest.mark.api
    @pytest.mark.regression
    def test_request_nonexistent_film(self, api_config: Dict[str, Any]) -> None:
        """
        Тест запроса несуществующего фильма

        Args:
            api_config: Конфигурация API с базовым URL и заголовками
        """
        with allure.step("Отправить GET запрос для несуществующего фильма"):
            url = f"{api_config['base_url']}/api/v2.2/films/29999999999"

            response = requests.get(
                url,
                headers=api_config["headers"]
            )

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400, (f"Ожидался статус 400, "
                                                 f"получен {response.status_code}")

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert "message" in response_data, ("В ответе отсутствует "
                                                "сообщение об ошибке")
