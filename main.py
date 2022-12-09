import sqlite3 as sq
import sys
from SQL_queries_data import vessel_table, catch_table, vessel_data, \
    insert_into_vessel, catch_data, insert_into_catch, \
    select_1, select_2, select_3, select_4, select_5


def create_database(db: str):
    """Функция для создания базы данных судового суточного донесения"""
    with sq.connect(db) as con:
        cur = con.cursor()
        cur.execute(vessel_table)
        cur.execute(catch_table)


def populate_database(db: str):
    """Функция заполнения базы данных """
    with sq.connect(db) as con:
        cur = con.cursor()
        cur.executemany(insert_into_vessel, vessel_data)
        cur.executemany(insert_into_catch, catch_data)


def get_query_result(db: str, q: int) -> any:
    """Функция получения результата запроса к базе данных"""
    with sq.connect(db) as con:
        cur = con.cursor()
        if q == 1:
            while True:
                try:
                    min_n, max_n = map(int, input('Введите диапазон веса улова через пробел:').split())
                    cur.execute(select_1.format(min_n, max_n))
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        return rows
                    else:
                        return ' в БД нет такого диапазона весов'
                except ValueError:
                    return 'Ошибка ввода. '

        elif q == 2:
            s = input('Введите название рыбы:\n').capitalize()
            cur.execute(select_2.format(s))
            rows = cur.fetchall()
            if len(rows) != 0:
                return rows
            else:
                return 'Таких рыб нет в БД'
        elif q == 3:
            cur.execute(select_3)
            rows = cur.fetchall()
            if len(rows) != 0:
                return rows
            else:
                return 'В БД пусто'
        elif q == 4:
            cur.execute(select_4)
            rows = cur.fetchall()
            if len(rows) != 0:
                return rows
            else:
                return 'В БД пусто'

        elif q == 5:
            s = input('Введите бортовой номер судна:\n')
            cur.execute(select_5.format(s))
            rows = cur.fetchall()
            if len(rows) != 0:
                return rows
            else:
                return 'Данные по запросу не найдены в БД'
        else:
            sys.exit()


def choose_command() -> int:
    """Функция выбора команды для вывода в консоль"""
    task = """
    Программа по требованию выдает списки:
    1. В которых вес лежит в заданном пользователем диапазоне
    2. Название рыбы совпадает с задаваемым пользователем, 
       отсортированного в порядке возрастания веса вылова.
    3. Вывести данные, когда был самый большой улов.
    4. Вывести данные, когда был самый маленький улов.
    5. Вывести данные по заданному пользователем бортовому номеру, 
       отсортированного в порядке возрастания веса вылова.
    Для выхода из программы введите 0
    Выберете, какой список Вы хотите получить, введите число от 1 до 5:
    """
    while True:
        try:
            user_query = int(input(task))
            if user_query in range(0, 6):
                break
            else:
                print('Неверный ввод!')
        except ValueError:
            print('Ошибка ввода. Должно быть целое число!')

    return user_query


def check_database(db: str) -> int:
    """Функция проверки базы данных на заполненность данными"""
    with sq.connect(db) as con:
        cur = con.cursor()
        sql = "SELECT * FROM catch;"
        num = len(cur.execute(sql).fetchall())
        return num


if __name__ == "__main__":
    name_db = "fish_catch.db"
    create_database(name_db)
    if not check_database(name_db):
        populate_database(name_db)
    while True:
        output = get_query_result(name_db, choose_command())
        print('Полученный результат:\n', output)
        s = input('Вы желаете еще что-то получить из базы данных, введите "да" или "нет"\n')
        if s in ('Да,да'):
            pass
        else:
            break
