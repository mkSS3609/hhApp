import random
import sys
from datetime import date


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        today = date.today()
        b_date = date.fromisoformat(self.birth_date)
        age = today.year - b_date.year
        if (today.month, today.day) < (b_date.month, b_date.day):
            age -= 1
        return age

    def save_to_db(self, db):
        sql = """
        INSERT INTO employees (full_name, birth_date, gender)
        VALUES (%s, %s, %s)
        ON CONFLICT (full_name, birth_date) DO NOTHING;
        """
        try:
            db.cur.execute(sql, (self.full_name, self.birth_date, self.gender))
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            print(e)
            sys.exit(1)

    def to_tuple(self):
        return (self.full_name, self.birth_date, self.gender)

    @staticmethod
    def generate(special=False):
        names = ["Ivanov", "Petrov", "Sidorov", "Kuznetsov", "Smirnov", "Popov", "Vasiliev", "Morozov", "Antonov"]
        first_names = ["Petr", "Ivan", "Alexey", "Sergey", "Dmitry", "Anna", "Maria", "Olga", "Elena", "Tatiana"]
        patronymics = ["Ivanovich", "Petrovich", "Alekseevich", "Sergeevich", "Dmitrievich", "Ivanovna", "Petrovna"]

        if special:
            full_name = f'F{random.choice(names)} {random.choice(first_names)} {random.choice(patronymics)}'
            gender = 'Male'
        else:
            full_name = f'{random.choice(names)} {random.choice(first_names)} {random.choice(patronymics)}'
            gender = random.choice(['Female', 'Male'])

        year = random.randint(1950, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth_date = f'{year}-{month}-{day}'
        return Employee(full_name, birth_date, gender)

    @classmethod
    def batch_save(cls, db, employees):
        sql = """
        INSERT INTO employees (full_name, birth_date, gender)
        VALUES (%s, %s, %s) ON CONFLICT (full_name, birth_date) DO NOTHING; \
        """
        data = [emp.to_tuple() for emp in employees]

        try:
            db.cur.executemany(sql, data)
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            print(e)
            sys.exit(1)
