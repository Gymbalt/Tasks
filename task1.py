#!Тестовое задание №1
from utils import get_data_from_file, fill_data_in_file


def run_calculate(k: int):
    """Запуск расчета
    :param k: число неповторяющихся элементов
    :return:
    """
    data = [x for x in get_data_from_file()]

    for i in range(0, k):

        index = 0
        value = data[0]
        lenght = len(data)

        while index < lenght:
            if value == data[index]:
                data.pop(index)
                lenght -= 1
            else:
                index += 1
        data.append(value)

    print(data[len(data) - 3 - 1:len(data)])
    # with open('result_task1.txt', 'w') as f:
    #     for x in data:
    #         f.write(str(x) + '\n')


if __name__ == "__main__":
    fill_data_in_file()
    run_calculate(4)
