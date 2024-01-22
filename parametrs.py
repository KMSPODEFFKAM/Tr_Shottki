import sqlite3

def parametrs_tranzitions(row):
    '''Параметры транзистора'''
    db = sqlite3.connect(f"tranzitions.db")
    cur = db.cursor()
    sqlstr = f"SELECT * FROM T where id = {row}"
    name_col = [name for name in cur.execute(sqlstr).fetchall()]
    return name_col[0]
