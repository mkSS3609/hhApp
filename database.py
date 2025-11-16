import sys
import psycopg2


class Database:
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = '5432'
        self.DBNAME = 'employees_db'
        self.USER = 'postgres'
        self.PASSWORD = 'post'

        try:
            self.conn = psycopg2.connect(
                host=self.HOST,
                port=self.PORT,
                database=self.DBNAME,
                user=self.USER,
                password=self.PASSWORD
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'\nОшибка: {e}')
            print('Проверьте параметры подключения!\n')
            sys.exit(1)

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS employees (
            full_name VARCHAR(100) NOT NULL,
            birth_date DATE NOT NULL,
            gender VARCHAR(6) NOT NULL,
            CONSTRAINT unique_fio_date UNIQUE (full_name, birth_date)
        );
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            sys.exit(1)

    def get_all_employees(self):
        sql = """
        SELECT full_name, birth_date, gender,
        EXTRACT(YEAR FROM AGE(birth_date)) AS age
        FROM employees
        ORDER BY full_name ASC;
        """
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            sys.exit(1)

    def search_male_f(self):
        sql = """
        SELECT full_name, birth_date, gender
        FROM employees
        WHERE gender = 'Male' AND full_name LIKE 'F%';
        """
        try:
            self.cur.execute(sql)
            return len(self.cur.fetchall())
        except Exception as e:
            print(e)
            sys.exit(1)

    def create_index(self):
        sql = """
        CREATE INDEX IF NOT EXISTS idx_male_f ON employees (gender, full_name)
        WHERE full_name LIKE 'F%';
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            sys.exit(1)
