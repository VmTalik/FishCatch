import sqlite3 as sq
import sys
from SQL_queries_data import vessel_table, catch_table, vessel_data, \
    insert_into_vessel, catch_data, insert_into_catch


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

