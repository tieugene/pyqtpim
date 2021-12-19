from PySide2 import QtSql

STORE_SQL = '''
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        active INTEGER NOT NULL DEFAULT 0,
        name VARCHAR UNIQUE NOT NULL,
        connection VARCHAR UNIQUE NOT NULL
    )
    '''
# CREATE INDEX store_name ON store (name)
CATEGORY_SQL = '''
    CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR UNIQUE NOT NULL
    )
    '''
# CREATE INDEX category_name ON category (name)
ENTRY_SQL = '''
    CREATE TABLE IF NOT EXISTS entry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id REFERENCES store(id) NOT NULL,
        created DATETIME NOT NULL,
        dtstamp DATETIME NOT NULL,
        modified DATETIME NOT NULL,
        dtstart ANY NULL,
        due ANY NULL,
        completed DATETIME NULL,
        progress TINYINT NULL,
        priority TINYINT NULL,
        status TINYINT NULL,
        summary VARCHAR NOT NULL,
        location VARCHAR NULL,
        body TEXT NOT NULL
    )
    '''
ENTRYCAT_SQL = '''
    CREATE TABLE IF NOT EXISTS entrycat (
        entry_id REFERENCES entry(id) NOT NULL,
        category_id REFERENCES category(id) NOT NULL
    )
'''
# CREATE INDEX entrycat_entry ON entrycat (entry_id)
# CREATE INDEX entrycat_category ON entrycat (category_id)


def init_db():
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())

    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("pyqtpim.sqlite3")
    check(db.open)
    q = QtSql.QSqlQuery()
    check(q.exec_, STORE_SQL)
    check(q.exec_, CATEGORY_SQL)
    check(q.exec_, ENTRY_SQL)
    check(q.exec_, ENTRYCAT_SQL)
