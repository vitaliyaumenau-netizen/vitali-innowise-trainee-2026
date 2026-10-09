import psycopg2
from sqlalchemy import create_engine, text
from read_data import ReadData
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)


class DatabaseDataInsertScripts(ReadData):

    def __init__(self, filename: str, db_name: str, user: str, password: str, host: str, port: int ):
        super().__init__(filename)
        self._db_name = db_name
        self._conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        self._engine = create_engine(f"postgresql://{user}:{password}@localhost:{port}/{db_name}")
        self._cursor = self._conn.cursor()

    def insert_data(self, table_name: str):
        """
        Универсальная вставка данных в любую таблицу и любые колонки.
        :param table_name: имя базы дынных
        """
        data = super().read_data()
        columns = super().get_columns()
        if data.empty:
            return

        # Формируем SQL-запрос с именованными плейсхолдерами:
        # INSERT INTO users (id, birthday) VALUES (:id, :birthday)
        cols_str = ", ".join(columns)
        placeholders = ", ".join([f":{col}" for col in columns])
        sql = text(f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})")


        # Преобразуем кортежи/списки из read_data в словарь параметров
        formatted_data = data.to_dict(orient="records")

        # Контекстный менеджер engine.begin() автоматически делает commit
        # и выполняет rollback при возникновении любого исключения
        try:
            with self._engine.begin() as conn:
                conn.execute(sql, formatted_data)
        except Exception as e:
            logging.exception(f"Ошибка при вставке данных в {table_name}: {e}")
            raise

    @property
    def cursor(self):
        return self._cursor

    def close(self):
        self._conn.close()