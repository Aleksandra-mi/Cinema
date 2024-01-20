import sqlite3


def get_db_connection():
    # con = sqlite3.connect("cinema.sqlite")
    # f_damp = open('cinema.db', 'r', encoding='utf-8-sig')
    # damp = f_damp.read()
    # f_damp.close()
    # con.executescript(damp)
    # con.commit()

    return sqlite3.connect('cinema.sqlite')
