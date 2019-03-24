#!Тестовое задание №2
from datetime import datetime, timedelta
from utils import median, read_from_file, write_to_file, write_to_db, read_from_db, DataRow, parse_row
from typing import Iterable, Text
import random

DAY_S = 86400  # количество секунд в сутках
SAMPLING_SEC = 1  # дискретизация данных
WINDOW_SIZE = 86390  # размер окна


def generate_data(interval_in_seconds: int = 100, start_date: 'datetime' = None) -> Iterable[DataRow]:
    """Создание данных

    :param interval_in_seconds: размер данных, интервал в секундах
    :param start_date: дата и время начала данных
    :return итератор строк (ts, value)
    """
    if WINDOW_SIZE > interval_in_seconds:
        raise Exception(
            'Размер окна больше размера данных, должно быть WINDOW_SIZE <= размера данных!!!')

    start_date = start_date or datetime(2019, 1, 1, 0, 0, 0)
    end_date = start_date + timedelta(seconds=interval_in_seconds)

    while start_date < end_date:
        value = random.randint(0, 100)
        yield DataRow(start_date, value)
        start_date += timedelta(seconds=1)


def calc_summary_of_window(window: list, win_count: int) -> Text:
    """ Расчет всех статистических параметров
    :param win_count: счетчик окон
    :param window: список значений (окно)
    :return:
    """
    v_min = min(window)
    v_max = max(window)
    v_avg = sum(window) / WINDOW_SIZE
    v_median = median(window)

    return ('window: ' + str(win_count), 'Max: ' + str(v_max) + '; Min: ' + str(v_min) + '; Avg: ' + str(
        v_avg) + '; Mdn: ' + str(v_median))


def iterate_by_windows_days(data: Iterable[DataRow]) -> Iterable[DataRow]:
    """ Обработка окон и группировка по дням
    :param data: отсортированный по времени исходный список
    """

    if WINDOW_SIZE > DAY_S:
        raise Exception(
            'Размер окна больше суток, непонятно по какой дате группировать полученную статистику(min, max и т.д.)!!!')

    win_count = 0
    currently_day = None
    window = []
    for line in data:
        row = parse_row(line)  # получаем кортеж из даты и значения

        if currently_day is None:
            currently_day = row.time  # дата первого значения за сутки

        window.append(row.value)
        w_size = len(window)

        if w_size < WINDOW_SIZE:  # набираем окно
            continue
        else:
            if currently_day.day != row.time.day:
                window.clear()
                window.append(row.value)
                currently_day = row.time  # дата первого значения за сутки
                win_count = 0
            else:
                yield DataRow(row.time, calc_summary_of_window(window, win_count))
                win_count += 1
                window.pop(0)


def iterate_by_windows(data: Iterable[DataRow]) -> Iterable[DataRow]:
    """ Обработка окон
    :param data: отсортированный по времени исходный список
    """

    win_count = 0
    window = []
    for line in data:

        row = parse_row(line)  # получаем кортеж из даты и значения
        window.append(row.value)
        w_size = len(window)

        if w_size < WINDOW_SIZE:
            continue
        else:
            window.append(row.value)
            yield DataRow(row.time, calc_summary_of_window(window, win_count))
            win_count += 1
            window.pop(0)


def iterate(data: Iterable[DataRow], is_days: bool = False):
    """ Запуск итераций
    :param data: отсортированный по времени исходный список
    :param is_days: группировка по дням
    :return:
    """
    if is_days:
        write_to_file(iterate_by_windows_days(data), is_days=True, path='result.txt')
    else:
        write_to_file(iterate_by_windows(data), path='result.txt')


def run():
    # ===================== с группировкой по дням =====================================
    data = generate_data(172801)
    write_to_file(data)
    data = read_from_file()
    iterate(data, is_days=True)
    # ==================================================================================
    # ===================== без группировки по дням ====================================
    # data = generate_data(200)
    # write_to_file(data)
    # data = read_from_file()
    # iterate(data, is_days=False)
    # ==================================================================================


if __name__ == "__main__":
    run()
