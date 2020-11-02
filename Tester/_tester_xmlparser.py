#-*- coding: utf-8 -*-
# from __future__ import print_function
import re
from GitSearch.MyUtils import read_file

html = '/home/ubuntu/Desktop/CoCaBu/2.xml'

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
# html = read_file(html)
# parsed_html = BeautifulSoup(html)

# print (parsed_html.body.find('div', attrs={'class': 'organic__url-text'}).text)


import xml.etree.ElementTree as ET
root = ET.parse(html).getroot()
tag = root.tag
print(tag)
attributes = root.attrib
print(attributes)
version = attributes.get('version')
print('version : ', version)
for holiday in root.findall('group'):
    print(holiday)
    for element in holiday:
        ele_name = element.tag
        ele_value = holiday.find(element.tag).text
        print(ele_name, ' : ', ele_value)


# iterate over all nodes
for yandex in root.findall('yandexsearch'):


    attributes = yandex.attrib
    print(attributes)

    # access element - name
    name = yandex.find('name').text
    print('name : ', name)

    # access element - date
    date = holiday.find('date').text
    print('date : ', date)