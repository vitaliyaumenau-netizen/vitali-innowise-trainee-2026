import functools
import os
from typing import Any, Callable
import pandas as pd


class WorkingWithData:
    """Класс для первичного чтения данных из JSON-файлов и декорирования экспорта.

    Attributes:
        _df (pd.DataFrame): Датафрейм с загруженными исходными данными.
    """

    def __init__(self, filename: str) -> None:
        """Инициализирует экземпляр WorkingWithData и загружает данные из JSON.

        Args:
            filename (str): Имя файла JSON, находящегося в директории 'data/'.
        """
        self._df = pd.read_json(f"data/{filename}")
        self._df = self._df.where(pd.notnull(self._df), None)

    def read_data(self) -> pd.DataFrame:
        """Возвращает копию исходного датафрейма.

        Returns:
            pd.DataFrame: Копия загруженного датафрейма с данными.
        """
        return self._df.copy()

    def get_columns(self) -> pd.Index:
        """Возвращает список/индекс названий колонок загруженного датафрейма.

        Returns:
            pd.Index: Объект с названиями колонок датафрейма.
        """
        return self._df.columns

    @staticmethod
    def write_data_into_file(filename: str) -> Callable[..., Any]:
        """Декоратор для сохранения результатов выполнения SQL-функций в JSON.

        Принимает результат работы декорируемой функции в виде кортежа (data, columns),
        преобразует его в pandas.DataFrame и сохраняет в JSON-файл.

        Args:
            filename (str): Относительный или абсолютный путь к целевому JSON-файлу.

        Returns:
            Callable[..., Any]: Обёрнутая функция-декоратор.
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> tuple[Any, Any]:
                """Выполняет функцию базы данных и записывает результат в файл.

                Args:
                    *args: Произвольные позиционные аргументы.
                    **kwargs: Произвольные именованные аргументы.

                Returns:
                    tuple[Any, Any]: Кортеж из полученных данных и названий колонок.
                """
                result_data, result_columns = func(*args, **kwargs)

                # Создаём директорию, если она отсутствует
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                df = pd.DataFrame(result_data, columns=result_columns)
                df.to_json(filename, orient="records", indent=4, force_ascii=False)
                print(f"[Успех] Данные функции {func.__name__} сохранены в {filename}")

                return result_data, result_columns

            return wrapper

        return decorator