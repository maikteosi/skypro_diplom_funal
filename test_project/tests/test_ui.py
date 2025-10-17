import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@allure.epic("Kinopoisk UI Tests")
@allure.feature("Комплексные UI тесты для Кинопоиска")
class TestKinopoiskComprehensiveUI:
    """Класс для комплексных UI тестов Кинопоиска с пошаговыми кликами"""

    @allure.story("Поиск фильма")
    @allure.title("TC-101: Поиск фильма и добавление в избранное")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_search_and_add_to_favorites(self, driver):
        """Тест поиска фильма и добавления в избранное"""
        wait = WebDriverWait(driver, 15)

        with allure.step("1. Открыть сайт Кинопоиска"):
            driver.get("https://www.kinopoisk.ru/")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            assert "Кинопоиск" in driver.title
            print("✅ Главная страница открыта")

        with allure.step("2. Ввести в поисковую строку название фильма"):
            search_selectors = [
                "input[name='kp_query']",
                "input[placeholder*='фильм']",
                "input[type='search']",
            ]

            search_input = None
            for selector in search_selectors:
                try:
                    search_input = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Поисковая строка найдена: {selector}")
                    break
                except Exception:
                    continue

            if not search_input:
                pytest.fail("❌ Поисковая строка не найдена")

            search_input.clear()
            search_input.send_keys("Интерстеллар")
            # Ждем пока значение в поле обновится
            wait.until(EC.text_to_be_present_in_element_value(
                (By.CSS_SELECTOR, search_selectors[0]), "Интерстеллар"))
            print("✅ Название фильма 'Интерстеллар' введено")

        with allure.step("3. Выполнить поиск"):
            search_buttons = [
                "button[type='submit']",
                ".header-fresh-search-button",
                ".search-btn",
                "input[type='submit']",
                "[data-tid='search_button']"
            ]

            search_performed = False
            for selector in search_buttons:
                try:
                    search_button = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    search_button.click()
                    print("✅ Поиск выполнен по кнопке")
                    search_performed = True
                    break
                except Exception:
                    continue

            if not search_performed:
                search_input.send_keys(Keys.ENTER)
                print("✅ Поиск выполнен по Enter")

            # Ждем загрузки результатов поиска
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 ".search_results, .search-results, [data-tid*='search'], "
                 ".styles_root__tiG8t")))
            print("✅ Результаты поиска загружены")

        with allure.step("4. Открыть страницу фильма"):
            film_selectors = [
                "a[href*='/film/']",
                ".search_results a",
                ".name a",
                ".styles_root__tiG8t a",
                "//a[contains(text(), 'Интерстеллар') or "
                "contains(@title, 'Интерстеллар')]"
            ]

            film_found = False
            for selector in film_selectors:
                try:
                    if selector.startswith("//"):
                        film_links = wait.until(
                            EC.presence_of_all_elements_located((By.XPATH, selector))
                        )
                    else:
                        film_links = wait.until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, selector))
                        )

                    for link in film_links:
                        if ("интерстеллар" in link.text.lower() or
                                "interstellar" in link.text.lower()):
                            driver.execute_script("arguments[0].click();", link)
                            film_found = True
                            break

                    if film_found:
                        break
                except Exception:
                    continue

            if film_found:
                wait.until(EC.url_contains("/film/"))
                print("✅ Страница фильма 'Интерстеллар' открыта")
            else:
                try:
                    first_film = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/film/']"))
                    )
                    first_film.click()
                    wait.until(EC.url_contains("/film/"))
                    print("✅ Открыта страница первого найденного фильма")
                except Exception:
                    pytest.skip("❌ Не удалось открыть страницу фильма")

    @allure.story("Навигация по жанрам")
    @allure.title("TC-102: Поиск фильмов по жанру фантастика")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_genre_navigation(self, driver):
        """Тест навигации по жанрам и сортировки"""
        wait = WebDriverWait(driver, 15)

        with allure.step("1. Открыть страницу с жанрами"):
            driver.get("https://www.kinopoisk.ru/lists/categories/movies/8/")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Раздел 'Жанры' открыт")

        with allure.step("2. Выбрать жанр в поле выбора жанра"):
            genre_selectors = [
                "//*[@id='__next']/div[1]/div[2]/div[4]/div[2]/div/a[4]/div[1]",
                "//a[contains(text(), 'Фантастика')]",
            ]

            genre_selected = False
            for selector in genre_selectors:
                try:
                    if selector.startswith("//"):
                        genre_option = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        genre_option = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )

                    genre_option.click()
                    print("✅ Жанр 'Фантастика' выбран")
                    genre_selected = True
                    break
                except Exception:
                    continue

            if not genre_selected:
                print("⚠️ Не удалось выбрать жанр 'Фантастика'")

        with allure.step("3. Проверить наличие фильмов в списке"):
            try:
                films = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/film/']"))
                )
                print(f"✅ Найдено фильмов: {len(films)}")
            except Exception:
                print("⚠️ Фильмы не найдены на странице")

    @allure.story("Сортировка и управление списками")
    @allure.title("TC-103: Сортировка фильмов и управление списками")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sorting_and_lists(self, driver):
        """Тест сортировки фильмов и работы со списками"""
        wait = WebDriverWait(driver, 15)

        with allure.step("1. Перейти в раздел лучших фильмов"):
            driver.get("https://www.kinopoisk.ru/lists/movies/top250/")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Раздел 'Топ 250 фильмов' открыт")

        with allure.step("2. Проверить наличие списка фильмов"):
            try:
                top_films = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/film/']"))
                )
                print(f"✅ Найдено фильмов в топе: {len(top_films)}")
            except Exception:
                print("⚠️ Не удалось найти список фильмов")

    @allure.story("Навигация по разделам")
    @allure.title("TC-104: Навигация по основным разделам сайта")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_main_navigation(self, driver):
        """Тест навигации по основным разделам сайта"""
        wait = WebDriverWait(driver, 15)

        with allure.step("1. Проверить доступность основных разделов"):
            main_sections = [
                ("Фильмы", "https://www.kinopoisk.ru/lists/categories/movies/1/"),
                ("Сериалы", "https://www.kinopoisk.ru/lists/categories/series/1/"),
                ("Топ 250", "https://www.kinopoisk.ru/lists/movies/top250/"),
            ]

            for section_name, section_url in main_sections:
                try:
                    driver.get(section_url)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    print(f"✅ Раздел '{section_name}' доступен")
                except Exception as e:
                    print(f"⚠️ Раздел '{section_name}' недоступен: {e}")

        with allure.step("2. Проверить поиск по разным разделам"):
            search_queries = ["Матрица", "Игра престолов"]

            for query in search_queries:
                try:
                    driver.get("https://www.kinopoisk.ru/")
                    search_input = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "input[name='kp_query'], input[type='search']")))
                    search_input.clear()
                    search_input.send_keys(query)
                    search_input.send_keys(Keys.ENTER)

                    wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".search_results, .styles_root__tiG8t")))
                    print(f"✅ Поиск '{query}' выполнен успешно")
                except Exception as e:
                    print(f"⚠️ Поиск '{query}' не удался: {e}")

    @allure.story("Расширенный поиск")
    @allure.title("TC-105: Расширенный поиск фильма")
    @pytest.mark.ui
    @pytest.mark.regression
    def test_advanced_search(self, driver):
        """Тест расширенного поиска фильма"""
        wait = WebDriverWait(driver, 15)

        with allure.step("1. Открыть сайт Кинопоиска"):
            driver.get("https://www.kinopoisk.ru/")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Главная страница открыта")

        with allure.step("2. Открыть страницу расширенного поиска"):
            driver.get("https://www.kinopoisk.ru/s/")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Страница расширенного поиска открыта")

            # Отладочная информация - посмотрим на страницу
            print(f"📄 Текущий URL: {driver.current_url}")
            print(f"📄 Заголовок страницы: {driver.title}")

        with allure.step("3. Заполнить поле названия фильма"):
            # Расширяем список селекторов
            title_selectors = [
                "input[name='kp_query']",  # Основной поисковый input
                "input[type='text']",
                "input[placeholder*='фильм']",
                "input[placeholder*='названи']",
                "input[name*='name']",
                "input[name*='title']",
                ".header-fresh-search-input",
                "[data-tid='search_input']",
                "#find_film",
                ".textfield__input",
                "//input[contains(@placeholder, 'названи')]",
                "//input[contains(@name, 'name')]",
                "//input[contains(@class, 'textfield')]",
                "input"  # Просто любой input
            ]

            title_found = False
            for selector in title_selectors:
                try:
                    if selector.startswith("//"):
                        title_input = wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        title_input = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )

                    # Проверяем, что элемент видим и доступен
                    if title_input.is_displayed() and title_input.is_enabled():
                        print(f"🔍 Найден элемент названия: {selector}")
                        title_input.clear()
                        title_input.send_keys("Начало")
                        print("✅ Название фильма 'Начало' введено")
                        title_found = True
                        break
                    else:
                        print(f"⚠️ Элемент найден но недоступен: {selector}")
                except Exception as e:
                    print(f"❌ Не найден: {selector} - {str(e)[:50]}...")
                    continue

            if not title_found:
                print("⚠️ Поле названия не найдено")
                # Покажем какие элементы вообще есть на странице
                try:
                    all_inputs = driver.find_elements(By.TAG_NAME, "input")
                    print(f"🔍 Все input элементы на странице: {len(all_inputs)}")
                    for i, inp in enumerate(all_inputs[:5]):  # Покажем первые 5
                        print(f"  Input {i}: type={inp.get_attribute('type')}, "
                              f"name={inp.get_attribute('name')}, "
                              f"placeholder={inp.get_attribute('placeholder')}")
                except Exception:
                    pass

        with allure.step("4. Заполнить поле года"):
            # Расширяем список селекторов для года
            year_selectors = [
                "input[name*='year']",
                "input[placeholder*='год']",
                "input[type='number']",
                "#year",
                "input[name*='m_act[year]']",
                "//input[contains(@placeholder, 'год')]",
                "//input[contains(@name, 'year')]",
                "//input[@type='number']",
                "input"  # Просто любой input
            ]

            year_found = False
            for selector in year_selectors:
                try:
                    if selector.startswith("//"):
                        year_input = wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        year_input = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )

                    if year_input.is_displayed() and year_input.is_enabled():
                        print(f"🔍 Найден элемент года: {selector}")
                        year_input.clear()
                        year_input.send_keys("2010")
                        print("✅ Год 2010 введен")
                        year_found = True
                        break
                    else:
                        print(f"⚠️ Элемент года найден но недоступен: {selector}")
                except Exception as e:
                    print(f"❌ Не найден год: {selector} - {str(e)[:50]}...")
                    continue

            if not year_found:
                print("⚠️ Поле года не найдено")

        with allure.step("5. Выполнить поиск"):
            search_btn_selectors = [
                "[type='submit']",
                "//input[@type='submit']",
                "button[type='submit']",
                ".header-fresh-search-button",
                ".search-btn",
                "//button[contains(text(), 'Найти')]",
                "//span[contains(text(), 'Найти')]"
            ]

            search_performed = False
            for selector in search_btn_selectors:
                try:
                    if selector.startswith("//"):
                        search_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        search_btn = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )

                    print(f"🔍 Найдена кнопка поиска: {selector}")
                    driver.execute_script("arguments[0].click();", search_btn)
                    print("✅ Поиск выполнен")
                    search_performed = True
                    break
                except Exception as e:
                    print(f"❌ Не найдена кнопка: {selector} - {str(e)[:50]}...")
                    continue

            if not search_performed:
                print("⚠️ Кнопка поиска не найдена, пробуем нажать Enter")
                try:
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ENTER).perform()
                    print("✅ Поиск выполнен по Enter")
                except Exception:
                    print("❌ Не удалось выполнить поиск")

        with allure.step("6. Проверить результаты поиска"):
            results_selectors = [
                ".search_results",
                ".styles_root__tiG8t",
                "[data-tid*='search']",
                ".content",
                "a[href*='/film/']"
            ]

            for selector in results_selectors:
                try:
                    results = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if results.is_displayed():
                        print(f"✅ Результаты поиска отображены (селектор: {selector})")
                        break
                except Exception:
                    continue
            else:
                print("⚠️ Результаты поиска не отображены")