#!Тестовое задание №2
from datetime import datetime, timedelta
from utils import median, read_data_from_file, write_result, write_data_in_file, Point
from typing import Iterable

import random

# import sqlite3


SAMPLING_SEC = 1
WINDOW_SIZE = 86390


def generate_data(interval_in_seconds: int = 100, start: datetime = None) -> Iterable[Point]:
    """ Создание данных
    :param datetime start: дата и время начала данных
    :param int interval_in_seconds: размер данных, интервал в секундах
    :return Iterable[tuple]
    """
    start = start or datetime(2019, 1, 1, 0, 0, 0)
    end = start + timedelta(seconds=interval_in_seconds)

    while start < end:
        value = random.randint(0, 100)
        yield (start, value)
        start += timedelta(seconds=SAMPLING_SEC)


def calculate_summary_of_window(list_of_data: list, count: int, path: str = 'result.txt'):
    """ Расчет всех статистических параметров
    :param count: счетчик окон
    :param list_of_data: список значений (окно)
    :return:
    """
    min_value = min(list_of_data)
    max_value = max(list_of_data)
    sum_value = sum(list_of_data)
    sum_value = sum_value / WINDOW_SIZE
    median_value = median(list_of_data)
    write_result(min_value, max_value, sum_value, median_value, count, path)


def iterate_by_windows(data: Iterable[Point]):
    """ Обработка окон
    :param data: отсортированный по времени
    """

    if WINDOW_SIZE > 86400:
        raise Exception(
            'Размер окна больше суток, непонятно по какой дате группировать полученную статистику(min, max и т.д.)!!!')

    count_window = 0
    currently_day = None
    window = []
    for dt, val in data:

        if currently_day == None:
            currently_day = dt  # дата первого значения за сутки

        window.append(val)
        w_size = len(window)

        if w_size < WINDOW_SIZE:
            continue
        else:
            if currently_day.day != dt.day:
                window.clear()
                window.append(val)
                currently_day = dt  # дата первого значения за сутки
                count_window = 0
            else:
                calculate_summary_of_window(window, count_window, str(dt.date()) + '.txt')
                count_window += 1
                window.pop(0)




def run():
    data = generate_data(259201)
    write_data_in_file(data)
    data = read_data_from_file()
    iterate_by_windows(data)


if __name__ == "__main__":
    run()
