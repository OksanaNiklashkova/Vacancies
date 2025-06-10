import psycopg2


def create_database(db_name: str, params: dict) -> None:
    """Создание базы данных"""
    conn = None
    try:
        # Подключаемся
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True

        # Формирование запроса
        with conn.cursor() as cur:
            try:
                cur.execute(f"DROP DATABASE IF EXISTS {db_name}")  # Удаляем БД
            finally:
                cur.execute(f"CREATE DATABASE {db_name}")  # Создаем БД
        print(f'База "{db_name}" успешно пересоздана!')

    except psycopg2.Error as e:
        print(f"Ошибка при создании БД: {e}")
        raise

    finally:
        if conn:
            conn.close()  # закрываем соединение


def create_table(db_name: str, params: dict) -> None:
    """Создание таблиц в базе данных"""
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE employers(
        employer_id varchar(20) PRIMARY KEY,
        name varchar(50) NOT NULL,
        url varchar(100) NOT NULL
        )"""
        )

    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE vacancies(
                id varchar(20) PRIMARY KEY,
                name varchar(100) NOT NULL,
                url varchar(100) NOT NULL,
                salary integer,
                requirements text,
                employer_id varchar(20)  NOT NULL,
                CONSTRAINT fk_vacancies_employer_id FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )"""
        )
    conn.commit()
    conn.close()


def fill_data(db_name: str, params: dict, table_name: str, data: list) -> None:
    """Сохранение данных о работодателях и вакансиях в базу данных"""
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        for item in data:
            if not item:  # Пропускаем пустые записи
                continue

            keys = list(item.keys())
            values = list(item.values())

            # Формируем строку с именами колонок
            columns = ", ".join(keys)
            # Формируем строку с плейсхолдерами
            placeholders = ", ".join(["%s"] * len(values))

            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """

            try:
                cur.execute(query, values)
            except psycopg2.Error as e:
                print(f"Ошибка при вставке данных: {e}")
                conn.rollback()
                raise

    conn.commit()
    print(f"Таблица {table_name} успешно сформирована")
    conn.close()
