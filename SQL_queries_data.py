"""Скрипт с SQL запросами и данными. База данных судового суточного донесения"""
"""
========================
Создание базы данных
========================
"""
vessel_table = """CREATE TABLE IF NOT EXISTS vessel (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vessel_name TEXT, 
                        side_number TEXT UNIQUE
                        );"""

catch_table = """CREATE TABLE IF NOT EXISTS catch (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fish_name TEXT,
                        catch_date TEXT,
                        weight REAL,
                        vessel_id INTEGER,
                        FOREIGN KEY (vessel_id) REFERENCES vessel (id)
                        );"""
"""
===============================
Внесение данных в базу данных
===============================
"""
insert_into_vessel = 'INSERT INTO vessel (vessel_name,side_number) values(?,?)'
vessel_data = [('Емеля', 'ПН-60'),
                    ('Грунтаг', 'ВГ-67'),
                    ('Варяг', 'ПР-76'),
                    ('Картет', 'РС-81'),
                    ]

insert_into_catch = 'INSERT INTO catch (fish_name, catch_date, weight, vessel_id) values(?, ?, ?, ?)'

catch_data = [
    ('Окунь', '2022-11-21', 20, 1),
    ('Треска', '2022-12-1', 19, 3),
    ('Терпуг', '2022-11-24', 23, 4),
    ('Окунь', '2022-11-29', 14, 2),
]

"""
===============================
Запросы к базе данных
===============================
"""
# выборка по заданному диапазону веса
select_1 = """SELECT fish_name, weight, catch_date, vessel_name, side_number 
                FROM catch INNER JOIN vessel
	              ON catch.vessel_id = vessel.id
               WHERE catch.weight BETWEEN {} AND {};
               """

# выборка по названию рыбы. Название совпадает с задаваемым пользователем,
# отсортированного в порядке возрастания веса вылова.
select_2 = """SELECT fish_name, weight, catch_date, vessel_name, side_number 
                FROM catch INNER JOIN vessel
	              ON catch.vessel_id = vessel.id
               WHERE catch.fish_name = '{}'
               ORDER BY catch.weight;
               """

# выборка данных, когда был самый большой улов.(Самые большие уловы входят в диапазон от 0.8 до 1 от максимального)
select_3 = """SELECT fish_name, weight, catch_date, vessel_name, side_number 
                FROM catch INNER JOIN vessel
	              ON catch.vessel_id = vessel.id
               WHERE catch.weight BETWEEN 0.8*(SELECT MAX(weight) from catch) AND
                                                (SELECT MAX(weight) from catch);
               """

# выборка данных, когда был самый маленький улов.
select_4 = """SELECT fish_name, weight, catch_date, vessel_name, side_number 
                FROM catch INNER JOIN vessel
	              ON catch.vessel_id = vessel.id
               WHERE catch.weight = (SELECT MIN(weight) from catch);
               """

# выборка по по заданному пользователем бортовому номеру,
#     отсортированного в порядке возрастания веса вылова.
select_5 = """SELECT fish_name, weight, catch_date, vessel_name, side_number 
                FROM catch INNER JOIN vessel
	              ON catch.vessel_id = vessel.id
               WHERE vessel.side_number = '{}'
               ORDER BY catch.weight;
               """
