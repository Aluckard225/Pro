from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    engine = db.Column(db.String, nullable=False)
    power = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String, nullable=False)
    drive = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    features = db.relationship('Feature', backref='car', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'color': self.color,
            'mileage': self.mileage,
            'engine': self.engine,
            'power': self.power,
            'transmission': self.transmission,
            'drive': self.drive,
            'price': self.price,
            'comfort': [f.feature for f in self.features if f.category == 'comfort'],
            'safety': [f.feature for f in self.features if f.category == 'safety'],
            'media': [f.feature for f in self.features if f.category == 'media']
        }

class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    feature = db.Column(db.String, nullable=False)

def init_db(app):
    with app.app_context():
        db.create_all()
        if Car.query.count() == 0:
            sample_cars = [
               {
                    "name": "Lada Granta",
                    "year": 2021,
                    "color": "Красный",
                    "mileage": 35000,
                    "engine": "1.6L 8V",
                    "power": 87,
                    "transmission": "Механика",
                    "drive": "Передний",
                    "price": 600000,
                    "comfort": ["Кондиционер", "Электроусилитель руля", "Регулировка сидений", "Подогрев зеркал"],
                    "safety": ["ABS", "Подушка безопасности водителя", "Иммобилайзер", "Сигнализация"],
                    "media": ["USB", "AUX", "Радио", "2 динамика"]
                },
                {
                    "name": "Ford Mustang 1965",
                    "year": 1965,
                    "color": "Красный",
                    "mileage": 95000,
                    "engine": "4.7L V8",
                    "power": 200,
                    "transmission": "Механика",
                    "drive": "Задний",
                    "price": 4500000,
                    "comfort": ["Кожаный салон"],
                    "safety": ["Ремни безопасности"],
                    "media": ["Радио"]
                },
                {
                    "name": "Lada Volga GAZ-24",
                    "year": 1985,
                    "color": "Бежевый",
                    "mileage": 120000,
                    "engine": "2.4L I4",
                    "power": 95,
                    "transmission": "Механика",
                    "drive": "Задний",
                    "price": 350000,
                    "comfort": ["Гидроусилитель руля", "Отделка кожей"],
                    "safety": ["Ремни безопасности"],
                    "media": ["Радио"]
                },
                {
                    "name": "DeLorean DMC-12",
                    "year": 1983,
                    "color": "Нержавеющая сталь",
                    "mileage": 45000,
                    "engine": "2.8L V6",
                    "power": 130,
                    "transmission": "Автомат",
                    "drive": "Задний",
                    "price": 25000000,
                    "comfort": ["Электростеклоподъемники", "Кожаный салон"],
                    "safety": ["Антиблокировочная система"],
                    "media": ["Кассетный плеер"]
                },
                {
                    "name": "ВАЗ-2101 (Жигули)",
                    "year": 1975,
                    "color": "Вишневый",
                    "mileage": 80000,
                    "engine": "1.2L I4",
                    "power": 62,
                    "transmission": "Механика",
                    "drive": "Задний",
                    "price": 250000,
                    "comfort": ["Отопление"],
                    "safety": ["Ремни безопасности"],
                    "media": []
                },
                {
                    "name": "УАЗ Патриот",
                    "year": 2021,
                    "color": "Зеленый",
                    "mileage": 35000,
                    "engine": "2.7L",
                    "power": 149,
                    "transmission": "Механика",
                    "drive": "Полный",
                    "price": 1900000,
                    "comfort": ["Кондиционер", "Подогрев сидений"],
                    "safety": ["ABS", "2 подушки безопасности"],
                    "media": ["USB", "Bluetooth"]
                },
                                {
                    "name": "Kia K5",
                    "year": 2022,
                    "color": "Серый",
                    "mileage": 12000,
                    "engine": "2.5L Turbo",
                    "power": 290,
                    "transmission": "Автомат",
                    "drive": "Передний",
                    "price": 3200000,
                    "comfort": ["Вентилируемые сиденья", "Панорамная крыша"],
                    "safety": ["Автопилот", "8 подушек безопасности"],
                    "media": ["12.3\" экран", "Apple CarPlay"]
                },
                                {
                    "name": "Genesis G90",
                    "year": 2023,
                    "color": "Черный",
                    "mileage": 5000,
                    "engine": "3.5L Twin-Turbo",
                    "power": 380,
                    "transmission": "Автомат",
                    "drive": "Полный",
                    "price": 8500000,
                    "comfort": ["Массаж сидений", "Отделка алькантарой"],
                    "safety": ["Система ночного видения"],
                    "media": ["21-дюймовый экран"]
                },
                {
                    "name": "Lada Priora",
                    "year": 2016,
                    "color": "Белый",
                    "mileage": 92000,
                    "engine": "1.6L 16V",
                    "power": 106,
                    "transmission": "Механика",
                    "drive": "Передний",
                    "price": 400000,
                    "comfort": ["Кондиционер", "Электростеклоподъемники", "Регулировка руля", "Круиз-контроль"],
                    "safety": ["ABS", "2 подушки безопасности", "Иммобилайзер", "Центральный замок"],
                    "media": ["CD-плеер", "USB", "Радио", "4 динамика"]
                },
                {
                    "name":"Lexus LX 570", 
                    "year":2018, 
                    "color":"Чёрный",
                    "mileage":65000,
                    "engine":"5.7L V8",
                    "power":367,
                    "transmission":"Автомат",
                    "drive":"Полный",
                    "price":6800000,
                    "comfort":["4-зонный климат", "Холодильник", "Отделка кожей", "Электрорегулировка сидений"],
                    "safety":["10 подушек", "Камера обзора", "Адаптивный круиз", "Система контроля давления"],
                    "media":["Mark Levinson", "12.3\" экран", "Навигация", "Bluetooth"]
                },
                {
                    "name":"Renault Logan", 
                    "year":2018, 
                    "color":"Серебристый",
                    "mileage":68000,
                    "engine":"1.6L 16V",
                    "power":102,
                    "transmission":"Автомат",
                    "drive":"Передний",
                    "price":850000,
                    "comfort":["Кондиционер", "Электростеклоподъемники", "Регулировка сидений", "Подогрев зеркал"],
                    "safety":["ABS", "ESP", "2 подушки безопасности", "Центральный замок"],
                    "media":["Bluetooth", "USB", "Радио", "4 динамика"]
                },
                {
                    "name":"Hyundai Creta", 
                    "year":2020, 
                    "color":"Серый",
                    "mileage":42000,
                    "engine":"2.0L",
                    "power":149,
                    "transmission":"Автомат",
                    "drive":"Передний",
                    "price":1500000,
                    "comfort":["Климат-контроль", "Электропакет", "Подогрев сидений", "Круиз-контроль"],
                    "safety":["ABS", "ESP", "6 подушек безопасности", "Камера заднего вида"],
                    "media":["Apple CarPlay", "Android Auto", "7\" экран", "Bluetooth"]
                },
                {
                    "name":"Toyota Camry", 
                    "year":2020, 
                    "color":"Серебристый",
                    "mileage":45000,
                    "engine":"2.5L Hybrid",
                    "power":218,
                    "transmission":"Автомат",
                    "drive":"Передний",
                    "price":2500000,
                    "comfort":["Климат-контроль", "Электропакет", "Подогрев сидений", "Регулировка руля"],
                    "safety":["ABS", "ESP", "6 подушек безопасности", "Система удержания полосы"],
                    "media":["Apple CarPlay", "Навигация", "12.3\" экран", "Bluetooth"]
                },
                {
                    "name":"BMW X5", 
                    "year":2019, 
                    "color":"Чёрный",
                    "mileage":78000,
                    "engine":"3.0L Diesel",
                    "power":249,
                    "transmission":"Автомат",
                    "drive":"Полный",
                    "price":4200000,
                    "comfort":["4-зонный климат", "Память сидений", "Вентиляция сидений", "Массаж сидений"],
                    "safety":["Круиз-контроль", "Камера 360", "Система ночного видения", "Автопарковщик"],
                    "media":["Harman Kardon", "Gesture Control", "Digital Key", "Wi-Fi hotspot"]
                },
                {
                    "name":"Porsche 911 Turbo S", 
                    "year":2022, 
                    "color":"Графитовый",
                    "mileage":12000,
                    "engine":"3.8L Twin-Turbo",
                    "power":650,
                    "transmission":"PDK",
                    "drive":"Полный",
                    "price":15000000,
                    "comfort":["18-регулируемые сиденья", "Керамические тормоза", "Спортивный руль", "Система старт-стоп"],
                    "safety":["Парктроники", "Камеры кругового обзора", "Адаптивный круиз", "Система ночного видения"],
                    "media":["Bose Surround", "Apple CarPlay", "Цифровая приборная панель", "Голосовое управление"]
                },
                {
                    "name":"Tesla Model 3", 
                    "year":2023, 
                    "color":"Белый",
                    "mileage":8000,
                    "engine":"Electric",
                    "power":351,
                    "transmission":"Автомат",
                    "drive":"Полный",
                    "price":4500000,
                    "comfort":["Панорамная крыша", "Подогрев всех сидений", "Бесключевой доступ", "Автопилот"],
                    "safety":["8 камер", "12 датчиков", "Автоаварийное торможение", "Контроль слепых зон"],
                    "media":["15.4\" сенсорный экран", "Игровая система", "Wi-Fi", "Мобильное приложение"]
                },
                {
                    "name":"Mercedes-Benz GLE", 
                    "year":2021, 
                    "color":"Синий",
                    "mileage":35000,
                    "engine":"3.0L Diesel",
                    "power":272,
                    "transmission":"9G-Tronic",
                    "drive":"Полный",
                    "price":5800000,
                    "comfort":["AIRMATIC", "Память сидений", "4-зонный климат", "Электрорегулировка руля"],
                    "safety":["Active Brake Assist", "Сигнализация внимания", "Камера 360°", "Система защиты пешеходов"],
                    "media":["MBUX", "Два 12.3\" экрана", "Augmented Reality", "Burmester звук"]
                },
                {
                    "name":"Audi RS6", 
                    "year":2020, 
                    "color":"Нардо Грей",
                    "mileage":28000,
                    "engine":"4.0L TFSI",
                    "power":600,
                    "transmission":"Tiptronic",
                    "drive":"Полный",
                    "price":8500000,
                    "comfort":["Массаж сидений", "Вентиляция", "4-зонный климат", "Электрохромное зеркало"],
                    "safety":["Преситинг", "Night Vision", "Парктроник 360°", "Ассистент движения в пробке"],
                    "media":["Virtual Cockpit", "MMI Touch", "Bang & Olufsen", "HUD проекция"]
                },
                {
                    "name": "Toyota Supra V(A90)",
                    "year": 2022,
                    "color": "Оранжевый",
                    "mileage": 15000,
                    "engine": "3.0L Twin-Scroll Turbo I6",
                    "power": 382,
                    "transmission": "Автомат",
                    "drive": "Задний",
                    "price": 7500000,
                    "comfort": ["Спортивные сиденья", "Кожаный салон", "Двухзонный климат-контроль", "Бесключевой доступ"],
                    "safety": ["Система стабилизации", "8 подушек безопасности", "Камера 360°", "Адаптивный круиз-контроль"],
                    "media": ["8.8\" сенсорный экран", "Apple CarPlay", "Android Auto", "12-канальный звук"]
                },
                {
                    "name": "ЗИС-110 (Лимузин Сталина)",
                    "year": 1949,
                    "color": "Чёрный",
                    "mileage": 12000,
                    "engine": "6.0L I8",
                    "power": 140,
                    "transmission": "Механика",
                    "drive": "Задний",
                    "price": 10000000,
                    "comfort": ["Деревянная отделка", "Шторки на окнах", "Диванные сиденья", "Интерьер из сукна"],
                    "safety": ["Бронированный кузов", "Пуленепробиваемые стекла", "Сигнализация"],
                    "media": ["Радиоприёмник", "Мегафон"]
                },
                {
                    "name": "Mazda MX-5 Miata",
                    "year": 2020,
                    "color": "Красный",
                    "mileage": 25000,
                    "engine": "2.0L Skyactiv-G",
                    "power": 184,
                    "transmission": "Механика",
                    "drive": "Задний",
                    "price": 3200000,
                    "comfort": ["Складная крыша", "Кожаный руль", "Подогрев сидений", "Круиз-контроль"],
                    "safety": ["Система курсовой устойчивости", "6 подушек безопасности", "Датчики давления"],
                    "media": ["7-дюймовый дисплей", "Bose звуковая система", "Bluetooth", "Навигация"]
                }
            ]
            for car_data in sample_cars:
                car = Car(
                    name=car_data['name'],
                    year=car_data['year'],
                    color=car_data['color'],
                    mileage=car_data['mileage'],
                    engine=car_data['engine'],
                    power=car_data['power'],
                    transmission=car_data['transmission'],
                    drive=car_data['drive'],
                    price=car_data['price']
                )
                db.session.add(car)
                db.session.commit()
                for category in ['comfort', 'safety', 'media']:
                    for feature in car_data[category]:
                        feat = Feature(
                            car_id=car.id,
                            category=category,
                            feature=feature
                        )
                        db.session.add(feat)
                db.session.commit()