#!Unit тесты
from utils import median, write_txt, read_txt, parse
from datetime import datetime
import unittest
import os.path

PATH_TXT = 'Time series.txt'


class UnitTests(unittest.TestCase):
    """Класс unit тестов для второй задачи"""

    def test_median(self):
        """ Проверка медианы
        :return:
        """
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = median(data)
        self.assertEqual(result, 4.5)

        data.pop(0)
        result = median(data)
        self.assertEqual(result, 5.0)

    def test_write_txt(self):
        """ Проверка записи в текстовый файл
        :return:
        """
        dt_real = datetime(2019, 1, 1, 0, 0, 0)
        l = ((dt_real, x) for x in range(4))
        write_txt(l)
        self.assertEqual(os.path.isfile(PATH_TXT), True)  # проверка записи в файл по умолчанию

    def test_read_txt(self):
        """ Проверка чтения данных из текстового файла
        :param self:
        :return:
        """
        data = read_txt(PATH_TXT)
        for row in data:
            self.assertEqual(type(row) == str, True)

    def test_parse(self):
        """ Проверка парсера строки
        :param self:
        :return:
        """
        dt_real = datetime(2019, 1, 1, 0, 0, 0)
        val_resl = 0
        row = str(dt_real) + '\t' + str(val_resl)
        dt_watch, vai_watch = parse(row)
        self.assertEqual(dt_real == dt_watch and val_resl == vai_watch, True)

    def __del__(self):
        """ Деструктор
        :param self:
        :return:
        """
        if os.path.isfile(PATH_TXT):
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), PATH_TXT)
            os.remove(path)  # удаляем тестовый файл Time series.txt


def run():
    test = UnitTests()
    test.test_median()
    test.test_write_txt()
    test.test_read_txt()
    test.test_parse()


if __name__ == "__main__":
    run()
