#!Вспомогательные ф-ии
from datetime import datetime
from typing import Iterable, Tuple

import random

Point = Tuple[datetime, float]
DB_NAME = ":memory:"


def median(list_of_data: list) -> float:
    """ Расчет медианы
    :param list_of_data: список значений (окно)
    :return: медиана
    """

    if len(list_of_data) % 2 == 0:
        mdn1 = list_of_data[int(len(list_of_data) / 2 - 1)]
        mdn2 = list_of_data[int(len(list_of_data) / 2)]
        return (mdn1 + mdn2) / 2
    else:
        return list_of_data[int(len(list_of_data) // 2)][1]


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


def write_data_in_file(data: Iterable, path: str = 'Time series.txt'):
    """ Запись данных в текстовый файл.
    :param path: путь к файлу
    :param data: набор данных
    """

    with open(path, 'w') as f:
        for tup in data:
            f.write(str(tup[0]) + '\t' + str(tup[1]) + '\n')


def read_data_from_file(path: str = 'Time series.txt') -> Iterable[Point]:
    """ Запись данных в текстовый файл.
    :param path: путь к файлу
    :return Iterable[tuple]
    """

    try:
        with open(path, 'r') as f:
            for line in f:
                yield datetime.strptime(line.split('\t')[0], '%Y-%m-%d %H:%M:%S'), float(line.split('\t')[1])
    except IOError:
        print('An IOError has occurred!')
    except Exception:
        print('An Exception has occurred!')


def fill_data_in_file(path: str = 'Series.txt'):
    """Запись данных в текстовый файл.
    :param path: путь к файлу
    """

    with open(path, 'w') as f:
        for x in range(0, 20):
            f.write(str(random.randint(0, 100)) + '\n')


def get_data_from_file(path: str = 'Series.txt') -> Iterable[int]:
    """Запись данных в текстовый файл.
    :param path: путь к файлу
    :return Iterable[int]
    """

    try:
        with open(path, 'r') as f:
            for line in f:
                yield float(line)
    except IOError:
        print('An IOError has occurred!')
    except Exception:
        print('An Exception has occurred!')


def write_result(min_value: float, max_value: float, avg_value: float, median_value: float, count: int,
                 path: str = 'result.txt'):
    """ Запись результата
    :param min_value: минимум
    :param max_value: максимум
    :param avg_value: среднее
    :param median_value: медиана
    :param count: счетчик окон
    :param path: путь к файлу
    :return:
    """

    with open(path, 'a') as f:
        f.write('=======window======= :' + str(count) + '\n')
        f.write('Max: ' + str(max_value) + '; Min: ' + str(min_value) + '; Avg: ' + str(avg_value) + '; Mdn: ' + str(
            median_value) + '\n')
