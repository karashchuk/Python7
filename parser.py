import os
import sqlite3
import urllib.request
from xml.etree import ElementTree as ET
from collections import OrderedDict, namedtuple
# парсим документ
with open('cities.xml', 'r', encoding='utf-8') as f:
    tree = ET.parse(f)
print (tree)

# гуляем по дереву
root = tree.getroot()
countries = []
'''for country in root.findall('country'):
    countries.append(country.get('name'))
    #idm = country.find('city').attrib['id']
    #strana= country.find('city').attrib['country']
    #name1 = country.get('name')'''
#print (countries)
'''for city in tree.findall('//city'):
    gorod = city.text
    #name = country.get('name')
    idm = city.attrib['id']
    strana= city.attrib['country']
    #name1 = country.get('name')
    print (strana,idm,gorod)  '''
#for ms  in tree.iter('city'):
#	print (ms.tag, ms.attrib)
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
createbase('mydb')
n = input ('Введите название страны:  ')
for elem in tree.find('country[@name="' + n +'"]'):
    print (elem.attrib['id'],elem.text)
