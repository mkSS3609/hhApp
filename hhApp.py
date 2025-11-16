import sys
import time
from database import Database
from employee import Employee


def main():
    modes = ['help', '1', '2', '3', '4', '5', '6']

    if len(sys.argv) < 2:
        print('\nОшибка: не указан режим работы')
        print(f'Доступные режимы: {', '.join(modes)}')
        print('Пример запуска: python hhApp.py help\n')
        sys.exit(1)

    mode = sys.argv[1]

    if mode not in modes:
        print('Ошибка: указан неверный режим работы')
        print(f'Доступные режимы: {', '.join(modes)}')
        sys.exit(1)

    if mode == 'help':
        print('\nСправка по режимам:')
        print(' 1 - Создание таблицы сотрудников')
        print(' 2 - Добавление одного сотрудника')
        print('\tПример: python hhApp.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male')
        print(' 3 - Вывод всех сотрудников')
        print(' 4 - Автогенерация справочника сотрудников')
        print(' 5 - Результат выборки из таблицы по критерию: пол мужской, Фамилия начинается с "F" + замер времени')
        print(' 6 - Оптимизация и сравнение времени выполнения')
        print('\n\tПример запуска: python hhApp.py 1\n')
        sys.exit(0)

    print('\nПодключение к базе данных...', end='')
    db = Database()
    print('Успешно!')

    print(f'Запущен режим {mode}: ', end='')

    if mode == '1':
        print('Создание таблицы')
        db.create_table()
        print('Таблица создана! / Таблица уже существует!\n')
    elif mode == '2':
        print('Добавление сотрудника')
        if len(sys.argv) != 5:
            print('\nОшибка: Проверьте переданные параметры!')
            print('\tПример: python hhApp.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male\n')
            sys.exit(1)
        emp = Employee(sys.argv[2], sys.argv[3], sys.argv[4])
        print(sys.argv[2])
        print(f'Возраст: {emp.calculate_age()} лет/год(а)')
        emp.save_to_db(db)
        print('Сотрудник добавлен! / Запись уже существует!\n')
    elif mode == '3':
        print('Список сотрудников')
        rows = db.get_all_employees()
        if not rows:
            print('Записи отсутствуют!\n')
            sys.exit(1)
        print('=' * 80)
        for row in rows:
            print(f'{row[0]:<30} | {row[1]} | {row[2]:<6} | {int(row[3]):<3} лет/год(а)')
        print('=' * 80 + '\n')
    elif mode == '4':
        print('Автогенерация')
        print('Генерация...', end='')
        employees = []
        for _ in range(1_000_000):
            emp = Employee.generate(special=False)
            employees.append(emp)
        for _ in range(100):
            emp = Employee.generate(special=True)
            employees.append(emp)
        if employees:
            print('Успешно!')
        else:
            print('Ошибка в генерации\n!')
            sys.exit(1)
        print('Пакетная отправка...', end='')
        Employee.batch_save(db, employees)
        print('Успешно!\n')
    elif mode == '5':
        print('Результат выборки')
        print('Пол Male, Фамилия начинается с "F"')
        start = time.time()
        count_smf = db.search_male_f()
        finish = time.time()
        print(f'Время выполнения: {finish - start} сек')
        if not count_smf:
            print('Не найдено ни одного сотрудника!\n')
            sys.exit(1)
        print(f'Кол-во подходящих сотрудников - {count_smf}\n')
    elif mode == '6':
        print('Оптимизация')
        start = time.time()
        db.search_male_f() # режим 5
        finish = time.time()
        result_before = finish - start
        print(f'До оптимизации: {result_before} сек')
        db.create_index() # оптимизация
        start = time.time()
        db.search_male_f() # режим 5
        finish = time.time()
        result_after = finish - start
        print(f'После оптимизации: {result_after} сек')
        print(f'Стало быстрее в ~ {int(result_before // result_after)} раза')
        print('\nОБЪЯСНЕНИЕ:')
        print('- Создан частичный индекс по (gender, full_name) с условием WHERE full_name LIKE "F%"')
        print('- Индекс используется ТОЛЬКО для запросов с "F%" и "Male"')
        print('- PostgreSQL не сканирует всю таблицу, а идёт по индексу')
        print('- Подтверждено замерами времени\n')


if __name__ == '__main__':
    main()
