import sqlite3
import os

class Database:
    def __init__(self, db_name="abh_system.db"):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor

    def fetchall(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def initialize_tables(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                capacity INTEGER NOT NULL,
                monthly_rent REAL NOT NULL,
                status TEXT DEFAULT 'available'
            )
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT,
                id_number TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'active'
            )
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS leases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                monthly_rent REAL NOT NULL,
                deposit REAL NOT NULL,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (tenant_id) REFERENCES tenants(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lease_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TEXT NOT NULL,
                payment_type TEXT NOT NULL,
                month_covered TEXT,
                notes TEXT,
                FOREIGN KEY (lease_id) REFERENCES leases(id)
            )
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS utilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                utility_type TEXT NOT NULL,
                reading REAL NOT NULL,
                reading_date TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
