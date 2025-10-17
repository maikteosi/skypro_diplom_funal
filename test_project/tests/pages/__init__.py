# Этот файл делает директорию pages Python пакетом
from .base_page import BasePage
from .main_page import MainPage
from .search_page import SearchPage

__all__ = ['BasePage', 'MainPage', 'SearchPage']
