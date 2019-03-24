from utils import median, write_to_file, read_from_file, DataRow
from datetime import datetime
import unittest
import os.path


class UtilsTestCase(unittest.TestCase):
    """Класс unit тестов для второй задачи"""

    def test_median(self):
        """ Проверка медианы"""
        data = [8, 1, 5, 3, 4, 2, 6, 7, 1, 9]
        result = median(data)
        self.assertEqual(result, 4.5)

        data.pop(0)
        result = median(data)
        self.assertEqual(result, 5.0)

    def test_write_read_file(self):
        """ Проверка записи в/чтения из текстового файла"""
        dt_real = datetime(2019, 1, 1, 0, 0, 0)
        filename = './_utils_test.txt'
        origin_data = list(DataRow(dt_real, x) for x in range(4))

        write_to_file(data=origin_data, path=filename)
        self.assertEqual(os.path.isfile(filename), True, msg=f'Файл {filename!r} не был создан.')

        data = list(read_from_file(path=filename))
        self.assertListEqual(origin_data, data, msg='Оригинальные данные не совпадают со считанными из файла.')

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()
