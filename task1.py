#!Тестовое задание №1


def run(k: int, size: int):
    """Запуск расчета
    :param size: количество значений в списке
    :param k: число неповторяющихся элементов
    :return:
    """

    data = [(x // 2) for x in range(size)]

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

    print(data[len(data) - k:len(data)])


if __name__ == "__main__":
    run(5, 30)
