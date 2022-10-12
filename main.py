import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Stock, Shop, Sale, Book

DSN = 'postgresql://postgres:123456@localhost:5432/postgres'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

# Функция которая ищет либо по номеру либо по части имени



def publisher_id():
    res = input(f'Введите имя или индификатор издателя: ')
    if res.isnumeric():
        query1 = session.query(Publisher).filter(Publisher.id == res)
        for i in query1.all():
            print(f'{res} - {i.name}')
    else:
        query1 = session.query(Publisher).filter(Publisher.name.like(f'%{res}%'))
        for i in query1.all():
            print(f'{i.id} - {i.name}')

publisher_id()


def book_shop():
    res = input(f'Введите имя или индификатор издателя: ')
    if res.isnumeric():
        sub = session.query(Shop.name).join(Stock, Book, Publisher).filter(Publisher.id == res)
        for i in sub:
            print(i.name)
    else:
        sub = session.query(Shop.name).join(Stock, Book, Publisher).filter(Publisher.name.like(f'%{res}%'))
        for i in sub:
            print(i.name)

book_shop()

