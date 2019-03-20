#!Вспомогательные ф-ии
from datetime import datetime
from typing import Iterable, Tuple, List

Point = Tuple[datetime, float]
DB_NAME = ":memory:"


def median(list_of_data: List[float]) -> float:
    """ Расчет медианы
    :param list_of_data: список значений (окно)
    :return: медиана
    """
    if len(list_of_data) % 2 == 0:
        mdn1 = list_of_data[int(len(list_of_data) / 2 - 1)]
        mdn2 = list_of_data[int(len(list_of_data) / 2)]
        return (mdn1 + mdn2) / 2
    else:
        return list_of_data[int(len(list_of_data) // 2)]


def write_data_in_db(conn: 'Connection', data: Iterable):
    """ Запись данных в БД.
    :param conn: подключение к БД sqlite
    :param data: набор данных
    """
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE telemetry(dt datetime, value real)""")

    # Вставляем множество данных в таблицу используя безопасный метод "?"
    cursor.executemany("""INSERT INTO telemetry VALUES (?,?)""", data)
    conn.commit()


def read_data_from_db(conn: 'Connection') -> Iterable[Point]:
    """ Чтение данных из БД.
    :param conn: подключение к БД sqlite
    :return Iterable[tuple]
    """
    cursor = conn.cursor()

    for row in cursor.execute("SELECT * FROM telemetry ORDER BY dt"):
        # Конвертируем строку dt в объект datetime
        yield datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), row[1]
    # print(cursor.fetchall()) # or use fetchone() or fetchmany(size=cursor.arraysize)


def write_txt(data: Iterable, path: str = 'Time series.txt'):
    """ Запись данных в текстовый файл.
    :param path: путь к файлу
    :param data: набор данных
    """
    with open(path, 'a') as f:
        for tup in data:
            f.write(str(tup[0]) + '\t' + str(tup[1]) + '\n')


def read_txt(path: str = 'Time series.txt') -> Iterable[str]:
    """ Чтение данных из текстового файла.
    :param path: путь к файлу
    :return str
    """
    try:
        with open(path, 'r') as f:
            for line in f:
                yield str(line)
    except IOError:
        print('An IOError has occurred!')
    except Exception:
        print('An Exception has occurred!')


def parse(string: str) -> Point:
    """ Преобразует str в Iterable[Point].
    :param string: строка
    :return tuple
    """
    return datetime.strptime(string.split('\t')[0], '%Y-%m-%d %H:%M:%S'), float(string.split('\t')[1])

