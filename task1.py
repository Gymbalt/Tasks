#!Тестовое задание №1
import random
from typing import List

N = 100  # количество значений в списке
K = 10  # число неповторяющихся элементов в выборке


def select1(data: List, k: int) -> List:
    """ Выборка первых k неповторяющихся элементов
    :param data: исходный список
    :param k: число неповторяющихся элементов в выборке
    :return:
    """
    result = []
    for v in data:
        if v not in result:
            result.append(v)
        if len(result) == k:
            break

    if len(result) < k:
        print('Найдено только ' + str(len(result)) + ' из ' + str(k) + ' неповторяющихся чисел(')

    return result


def next_random_value(data: List, max_val: int) -> int:
    """ Следующее случайное значение
    :param data: исходный список
    :param max_val:
    :return:
    """
    if max_val > 0:
        return data[random.randint(0, max_val - 1)]


def select2(data: List, k: int) -> List:
    """ Выборка k случайных неповторяющихся элементов
    :param data: исходный список
    :param k: число неповторяющихся элементов в выборке
    :return:
    """
    result = []
    for i in range(0, k):

        index = 0
        length = len(data) - i
        value = next_random_value(data, length)

        if value is not None:
            result.append(value)

        while index < length:
            if value == data[index]:
                data.pop(index)
                length -= 1
            else:
                index += 1

        data.append(value)

        if length == 0:
            print('Найдено только ' + str(len(result)) + ' из ' + str(k) + ' неповторяющихся чисел(')
            break

    return result


def run():
    """Запуск расчета"""

    data = [(x // 2) for x in range(N)]  # создаем список начальных данных c повторениями
    print(f'Origin data: {data}')

    arr1 = select1(data, K)
    print(f'Arr1: {arr1}')

    # изменяет текущий список
    arr2 = select2(data, K)
    print(f'Arr2: {arr2}')


if __name__ == "__main__":
    run()
