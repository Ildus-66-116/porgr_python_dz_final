"""Возьмите любые 1-3 задания из прошлых домашних заданий. Добавьте к ним логирование ошибок и полезной информации.
Также реализуйте возможность запуска из командной строки с передачей параметров. """
import logging
import sys

FORMAT = ('{levelname:<4} - {asctime}. В модуле "{name}" '
          'в строке {lineno:03d} функция "{funcName}()" записала сообщение: {msg}')


def is_leap(year: int):
    """
    Функция проверки на весокосность года
    :param year: year
    :return: True / False
    """
    return not (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0))


def valid(full_date: str):
    """
    Функция для проверки корректности даты
    :param full_date: day.month.year
    :return: True / False
    """
    try:
        date, month, year = (int(item) for item in full_date.split('.'))
        if year < 1 or year > 9999 or month < 1 or month > 12 or date < 1 or date > 31:
            return False
        if month in (4, 6, 9, 11) and date > 30:
            return False
        if month == 2 and is_leap(year) and date > 29:
            return False
        if month == 2 and not is_leap(year) and date > 28:
            return False
        return True
    except ValueError as e:
        logging.error(f"Произошла ошибка в valid: {e}")
        print('Не правильный формат даты, должно быть день.месяц.год!')


def nephrologies(date_to_loging: str):
    """
    Функция логирования
    :param date_to_loging: srt: date.moth.year
    :return: file.log
    """
    name_file = 'task_1.log'
    logging.basicConfig(filename=name_file, filemode='a', encoding='utf-8',
                        level=logging.INFO, format=FORMAT, style='{')
    logger = logging.getLogger(__name__)
    logger.info("Начало работы программы.")
    logger.info(date_to_loging)
    logger.info(valid(date_to_loging))
    logger.info("Программа завершила работу.")
    print(f'Вся информация внесена в {name_file}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        data = sys.argv[1]
        nephrologies(data)
        print(f'Дата {data} статус {valid(data)}')
    else:
        date_to_test = input('Введите дату в формате день.месяц.год: ')
        nephrologies(date_to_test)


