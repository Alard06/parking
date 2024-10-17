import os
import sqlite3
from random import choice


class DataBase:
    """ Запросы к БД """
    def __init__(self) -> None:
        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()
        self.create_table_db()
        self.columns = {'manufacture': ['name'], 'model': ['manufacture', 'name', 'transmission', 'gear']}
        self.transmission = ('АКПП', 'МКПП', 'Робот', 'Вариатор', )
        self.gear = ('Передний привод', 'Задний привод', '4WD', )

    def connect_db(self):
        """Соединение с БД"""
        with sqlite3.connect('parking.db') as db:
            return db

    def create_table_db(self) -> None:
        """Создание таблиц в базе данных, если их не существует"""
        query_list = list()
        query_list.append('''CREATE TABLE IF NOT EXISTS manufacture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
        )''')
        query_list.append('''CREATE TABLE IF NOT EXISTS model (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacture INTEGER NOT NULL,
        name TEXT,
        transmission TEXT,
        gear TEXT,
        FOREIGN KEY (manufacture) REFERENCES manufacture(id)
        )''')
        query_list.append('''CREATE TABLE IF NOT EXISTS parking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        presence BOOLEAN,
        model INTEGER,
        color TEXT,
        state_number TEXT,
        engine BOOLEAN,
        open_doors BOOLEAN
        )''')

        for query in query_list:
            self.connection.execute(query)
    
    def load_data(self):
        """Загрузка первичных записей в таблицы"""
        try:
            tables = ('manufacture', 'model')
            for table in tables:
                with open(f'data/{table}.txt', 'r', encoding='UTF-8') as file:
                    data_file = file.readlines()
                    print(table)
                    query = f'INSERT INTO {table} ({', '.join(self.columns[table])}) VALUES '
                    if table == 'model':
                        query_get_manufacture = f'SELECT id, name FROM manufacture'
                        self.cursor.execute(query_get_manufacture)
                        manufactures_temp = self.cursor.fetchall()
                        manufacture = {}

                        for item in manufactures_temp:
                            manufacture[item[1]] = item[0]
                        data_file = ''.join([i.replace('\n', '') for i in data_file]).split('Модели')
                        query_data = ''
                        for models in data_file:
                            models = models.split(':')
                            cars = set(models[-1].split(' '))
                            try:
                                cars.remove('')
                            except KeyError:
                                pass
                            self.add_models(models=cars, manufacture=models[0])
                    else:
                        for item in data_file:
                            query += f'({repr(item.lower()[:-1].replace(' ', ''))}), '

                        print(query)
                        self.connection.execute(query[:-2])
                        self.connection.commit()
                    print(f'Данные успешно добавлены в таблицу: {table}')
        except:
            print('Данные уже существуют. Попробуйте удалить файл с БД и попробуйте снова')
    
    def add_models(self, models: str, manufacture: str):
        query = f'SELECT id FROM manufacture WHERE name={repr(manufacture.replace(' ', '').lower())}'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if models:
            query_add_models = 'INSERT INTO model (manufacture, name, transmission, gear) VALUES '
            for model in models:
                query_add_models += f'({result[0]}, {repr(model)}, {repr(choice(self.transmission))}, {repr(choice(self.gear))}), '
            print(query_add_models)

            self.connection.execute(query_add_models[:-2])
            self.connection.commit()
            print('add models')
    
    def model_info(self, model_id: int) -> tuple:
        query = '''SELECT * FROM parking WHERE model = ?'''
        cursor = self.connection.execute(query, (model_id,))
        records = cursor.fetchall()
        print(records)
        return records
    
    def get_data_parking(self):
        """Получение записей в таблице"""
        query = '''SELECT p.id, p.presence, p.color, p.engine, p.open_doors, m.name AS model_name
                   FROM parking p
                   JOIN model m ON p.model = m.id'''
        cursor = self.connection.execute(query)
        records = cursor.fetchall()

        parking_data = []
        for record in records:
            parking_info = {
                "ID": record[0],
                "Наличие": "Да" if record[1] else "Нет",
                "Модель": record[5],
                "Цвет": record[2],
                "Двигатель": "Заведен" if record[3] else "Выключен",
                "Дверь": "Открыты" if record[4] else "Закрыты"
            }
            parking_data.append(parking_info)

        for data in parking_data:
            print(f"ID: {data['ID']}")
            print(f"Наличие: {data['Наличие']}")
            print(f"Модель: {data['Модель']}")
            print(f"Цвет: {data['Цвет']}")
            print(f"Двигатель: {data['Двигатель']}")
            print(f"Дверь: {data['Дверь']}")
            print()  # Пустая строка для разделения записей

    

    def add_parking(self, presence: bool, model: int, color: str, state_number: str, engine: bool, open_doors: bool) -> None:
        """Создание записи в таблице"""
        try:
            query = '''INSERT INTO parking (presence, model, color, state_number, engine, open_doors) 
                    VALUES (?, ?, ?, ?, ?, ?)'''
            
            self.connection.execute(query, (presence, model, color, state_number, engine, open_doors))
            self.connection.commit()
        except:
            print('Произошла ошибка в данных. Попробуйте проверить введенные данные и повторите снова.')

    def edit_parking(self, parking_id: int, presence: bool, model: int, color: str, state_number: str, engine: bool, open_doors: bool) -> None:
        """Редактирование машин на парковке"""
        try:
            query = '''UPDATE parking 
                    SET presence = ?, model = ?, color = ?, state_number = ?, engine = ?, open_doors = ? 
                    WHERE id = ?'''
            self.connection.execute(query, (presence, model, color, state_number, engine, open_doors, parking_id))
            self.connection.commit()
        except:
            print('Произошла ошибка в данных. Попробуйте проверить введенные данные и повторите снова.')
    
    def remove_parking(self, parking_id: int) -> None:
        """Удаление записи в таблице по ID"""
        try:
            query = '''DELETE FROM parking WHERE id = ?'''
            self.connection.execute(query, (parking_id,))
            self.connection.commit()
        except:
             print('Произошла ошибка в данных. Попробуйте проверить введенные данные и повторите снова.')
    
    def get_model_id(self, model: str) -> int:
        query = f'SELECT id FROM model WHERE name={repr(model)}'
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    
    def get_specific_car(self, model_id: int) -> dict:
        """Получение характеристик определенной машины и количество модели на парковке"""
        # Получаем информацию о модели
        query = '''SELECT m.name AS manufacture_name, mo.name AS model_name, mo.transmission, mo.gear
                   FROM model mo JOIN manufacture m ON mo.manufacture = m.id
                   WHERE mo.id = ?'''
        car_details = self.connection.execute(query, (model_id,)).fetchone()

        # Получаем количество машин данной модели на парковке
        count_query = '''SELECT COUNT(*) FROM parking WHERE model = ?'''
        count = self.connection.execute(count_query, (model_id,)).fetchone()[0]

        return {
            "car_details": car_details,
            "count": count
        }
    
    def get_all_models(self):
        """Вывод всех автомобилей из таблицы model"""
        query = '''SELECT id, name FROM model'''
        cursor = self.connection.execute(query)
        records = cursor.fetchall()

        for record in records:
            print(f"ID: {record[0]}")
            print(f"Модель: {record[1]}")
            print()  # Пустая строка для разделения записей



class Parking:
    """ Управление базой данных на парковке.
     Удаление, добавление, редактирование пользователем машин на парковке """
    def __init__(self) -> None:
        self.run_application = True
        self.info_user = self.__get_info_users()
        self.data_base = DataBase()

    def run(self) -> bool:
        """Запуск консольного приложения"""
        # os.system('cls||clear')
        while self.run_application:
            print(self.info_user)
            operation = str(input('Введите цифру операции: '))
            match operation:
                case '1':
                    self.data_base.get_data_parking()
                case '2':
                    try:
                        presense = bool(input('Машина находится на парковке? \n1 - да\n0 - нет\n\n>>> '))
                        model = str(input('Введите модель машины: \n>>> '))
                        color = str(input('Введите цвет машины:\n>>> '))
                        state_number = str(input('Введите гос номер машины:\n>>> '))
                        engine = bool(input('Машина заведена? \n1 - да\n0 - нет\n\n>>> '))
                        open_doors = bool(input('Машина открыта? \n1 - да\n0 - нет\n\n>>> '))
                        model = self.data_base.get_model_id(model=model)
                        self.data_base.add_parking(presence=presense,
                                                   model=model, 
                                                   color=color, 
                                                   state_number=state_number, 
                                                   engine=engine,
                                                   open_doors=open_doors
                                                   )
                    except:
                        print('Вы ошиблись в типе данных. Попробуйте снова.')
                case '3':
                    try:
                        id_car = int(input('Введите id машины, которую нужно удалить. \n\n>>> '))
                        self.data_base.remove_parking(parking_id=id_car)
                    except:
                        print('Вы ошиблись в типе данных. Попробуйте снова.')
                case '4':
                    try:
                        parking_id = int(input('Введите id записи, которую нужно изменить. \n\n>>> '))
                        presense = bool(input('Машина находится на парковке? \n1 - да\n0 - нет\n\n>>> '))
                        model = str(input('Введите модель машины: \n>>> '))
                        color = str(input('Введите цвет машины:\n>>> '))
                        state_number = str(input('Введите гос номер машины:\n>>> '))
                        engine = bool(input('Машина заведена? \n1 - да\n0 - нет\n\n>>> '))
                        open_doors = bool(input('Машина открыта? \n1 - да\n0 - нет\n\n>>> '))
                        model = self.data_base.get_model_id(model=model)
                        self.data_base.edit_parking(presence=presense,
                                                    model=model, 
                                                    color=color, 
                                                    state_number=state_number, 
                                                    engine=engine,
                                                    open_doors=open_doors,
                                                    parking_id=parking_id
                                                    )
                    except:
                        print('Вы ошиблись в типе данных. Попробуйте снова.')
                case '5':
                    self.data_base.get_all_models()
                    model_id = input('Введите id автомобиля, для получения более подробной информации о модели.\n>>> ')

                    data = self.data_base.get_specific_car(model_id=model_id)
                    print(f"""
Марка: {data['car_details'][0]}
Модель: {data['car_details'][1]}
Привод: {data['car_details'][3]}
КПП: {data['car_details'][2]}
Количество на парковке {data['count']} шт
""")
                case '6':
                    self.run_application = False
                case '7':
                    self.data_base.load_data()
            input('Нажмите на Enter.')
            os.system('cls||clear')
    
    def __get_info_users(self) -> str:
        """Получение информации для использования приложения"""
        with open('info.txt', 'r', encoding='UTF-8') as file:
            data = file.read()
            return data


if __name__ == '__main__':
    parking = Parking()
    parking.run()

