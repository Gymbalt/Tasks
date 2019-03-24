#!Вспомогательные ф-ии
from collections import namedtuple
from datetime import datetime
from typing import Iterable, Tuple, List

# RowType = Tuple[datetime, float]
DataRow = namedtuple('RowType', ('time', 'value'))
DB_NAME = ":memory:"


def median(window: List[float]) -> float:
    """ Расчет медианы
    :param window: список значений (окно)
    :return: медиана
    """
    window.sort()
    if len(window) % 2 == 0:
        mdn1 = window[int(len(window) / 2 - 1)]
        mdn2 = window[int(len(window) / 2)]
        return (mdn1 + mdn2) / 2
    else:
        return window[int(len(window) // 2)]


def parse_data_row(row: List) -> DataRow:
    return DataRow(
        datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), float(row[1]))


def parse_row(row: str) -> DataRow:
    """ Парсер списка
    :param row:
    :return:
    """
    time = datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S')
    value = float(row[1])
    return DataRow(time, value)


def write_to_db(conn: 'Connection', data: Iterable):
    """ Запись данных в БД
    :param conn: подключение к БД sqlite
    :param data: набор данных
    """
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE telemetry(dt datetime, value real)""")

    # Вставляем множество данных в таблицу используя безопасный метод "?"
    cursor.executemany("""INSERT INTO telemetry VALUES (?,?)""", data)
    conn.commit()


def read_from_db(conn: 'Connection', parser=parse_row) -> Iterable[DataRow]:
    """Чтение данных из БД
    :param conn: подключение к БД sqlite
    :return Iterable[DataRow]
    """
    cursor = conn.cursor()

    for row in cursor.execute("SELECT * FROM telemetry ORDER BY dt"):
        # Конвертируем строку dt в объект datetime
        yield parser(row)
        # yield DataRow(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), row[1])
    # print(cursor.fetchall()) # or use fetchone() or fetchmany(size=cursor.arraysize)


def write_to_file(data: Iterable[DataRow], is_days: bool = False, path: str = 'Time series.txt'):
    """ Запись данных в текстовый файл
    :param path: путь к файлу
    :param data: набор данных
    :param is_days:  группировка по дням
    :return:
    """

    if is_days:
        for row in data:
            file = open(str(row.time.date()) + '_' + path, 'a')
            file.write(f'{str(row.time)}\t{str(row.value)}\n')
            file.close()
    else:
        with open(path, 'w') as f:
            for row in data:
                f.write(f'{str(row.time)}\t{str(row.value)}\n')


def read_from_file(parser=parse_row, path: str = 'Time series.txt') -> Iterable[DataRow]:
    """ Чтение данных из текстового файла
    :param parser: функция парсер
    :param path: путь к файлу
    :return:
    """
    try:
        with open(path, 'r') as f:
            for line in f:
                row = line.split('\t')
                yield parser(row)
    except IOError as e:
        print('An IOError has occurred!', e)
    except Exception as e:
        print('An Exception has occurred!', e)
