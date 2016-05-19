
""" Яндекс.Погода

Есть публичный урл со списком городов:
http://weather.yandex.ru/static/cities.xml

Для этих городов можно получить данные о погоде, подставив id города в шаблон:
http://export.yandex.ru/weather-ng/forecasts/<id города>.xml

Необходимо написать скрипт, который:
1. Создает файл базы данных SQLite с следующей структурой данных (если файла 
   базы данных не существует):

    Погода
        id                  INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура днем    INTEGER
        Температура ночью   INTEGER

2. Скачивает и парсит XML со списком городов
3. Выводит список стран из файла и предлагает пользователю выбрать страну
4. Скачивает XML файлы погоды в городах выбранной страны
5. Парсит последовательно каждый из файлов и добавляет данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


Температура днем и температура ночью берется из 
forecast/day/day_part@day_short/temperature и 
forecast/day/day_part@night_short/temperature соответственно:

<forecast ...>
    <day date="...">
        <day_part typeid="5" type="day_short">
            <temperature>29</temperature> 
            ...
        </day_part>
        <day_part typeid="6" type="night_short">
            <temperature>18</temperature>
            ...
        </day_part>
    </day>
</forecast>

При повторном запуске скрипта:
- используется уже скачанный файл с городами
- используется созданная база данных, новые данные добавляются и обновляются

Важное примечание:

Доступ к данным в XML файлах происходит через простансво имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с простанствами имен удобно пользоваться такими функциями:

# Получим пространство имен из первого тега:
def gen_ns(tag):
    if tag.startswith('{'):
        ns, tag = tag.split('}')
        return ns[1:]
    else:
        return ''

tree = ET.parse(f)
root = tree.getroot()

# Определим словарь с namespace
namespaces = {'ns': gen_ns(root.tag)}

# Ищем по дереву тегов
for day in root.iterfind('ns:day', namespaces=namespaces):
    ...

"""

import os
import sqlite3
import urllib.request
from xml.etree import ElementTree as ET
from collections import OrderedDict, namedtuple
import datetime

def createbase(filename):
    with sqlite3.connect(filename) as conn:
        conn.execute("""
            create table project (
                id                  INTEGER PRIMARY KEY,
                city               VARCHAR(255),
                date                DATE,
                d_tem    INTEGER,
                n_tem   INTEGER
            );
            """)

with open('cities.xml', 'r', encoding='utf-8') as f:
    tree = ET.parse(f)
print (tree)

# гуляем по дереву
root = tree.getroot()
'''countries = []
for country in root.findall('country'):
    countries.append(country.get('name'))
    #idm = country.find('city').attrib['id']
    #strana= country.find('city').attrib['country']
    #name1 = country.get('name')
print (countries)'''
'''for city in tree.findall('//city'):
    gorod = city.text
    #name = country.get('name')
    idm = city.attrib['id']
    strana= city.attrib['country']
    #name1 = country.get('name')
    print (strana,idm,gorod)  '''
#for ms  in tree.iter('city'):
#   print (ms.tag, ms.attrib)
db_filename = 'mydb3.db'
if os.path.exists(db_filename) == False:
    createbase(db_filename)
n = input ('Введите название страны:  ')
conn = sqlite3.connect(db_filename)
for elem in tree.find('country[@name="' + n +'"]'):
    '''conn.execute("""
        insert into project (id, city, date, d_tem, n_tem) VALUES (?,?,?,?,?)""", (
            elem.attrib['id'], 
            elem.text, 
            datetime.date.today(),
            20,
            10
        )
    )
    conn.execute("""
        update project set city = ?, date = ?, d_tem = ? , n_tem = ? WHERE id = ?""", (
            elem.text, 
            datetime.date.today(),
            25,
            11,
            elem.attrib['id']
        )
    )'''

    if list(conn.execute("""select * from project WHERE id = ? """,(elem.attrib['id'],))):
        print ('Уже есть')
        conn.execute("""
            update project set city = ?, date = ?, d_tem = ? , n_tem = ? WHERE id = ?""", (
                elem.text, 
                datetime.date.today(),
                25,
                11,
                elem.attrib['id']
            )
        )
    else:
        conn.execute("""
            insert into project (id, city, date, d_tem, n_tem) VALUES (?,?,?,?,?)""", (
                elem.attrib['id'], 
                elem.text, 
                datetime.date.today(),
                20,
                10
            )
        )
    print (elem.attrib['id'], 
            elem.text, 
            datetime.date.today(),20,10)
conn.commit()
conn.close()

