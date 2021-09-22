import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
#print(dir(requests))
# модуль `get` відповідає за зчитування ресурса в об'єкт 'response'
#requests.get
# отримаємо сторінку розкладів 
url = 'https://knute.edu.ua/blog/read/?pid=1038&uk'
resp = requests.get(url)
#print(dir(resp))
resp.text[:500]
resp.encoding
resp.apparent_encoding
resp.encoding = resp.apparent_encoding
#print(resp.text[:500])
knteu_rasp_page = resp.text
# застосуємо html-парсер до завантаженої сторінки з розкладами 'knteu_rasp_page'
parsed_rasp = bs(knteu_rasp_page, features='html.parser')
#print(dir(parsed_rasp))
back = parsed_rasp.find('span', text='БАКАЛАВР')
rasp_table = back.find_parent('strong').find_parent('h3').findNextSibling('table')
#print(rasp_table)
# в результаті виділили таблицю з розкладом
rasp_lines = rasp_table.find_all('tr')
#print(rasp_lines)
# в першому елементі - 'шапка' таблиці
head = rasp_lines[0].find_all('td')
#print(head)
# вибираємо назви факультетів в список
fac_names = [name.text for name in head]
#print(fac_names)
# далі з 1 рядка йдуть строки с посиланнями по курсам
rasp_lines[1:]
#print(rasp_lines)
hrefs = [[a['href'], a.text.split('\n')[0]] for a in rasp_lines[1].find_all('a')]
#print(hrefs)


back_mag = parsed_rasp.find('span', text='МАГІСТР')
rasp_table_mag = back_mag.find_parent('strong').find_parent('h3').findNextSibling('table')
rasp_lines_mag = rasp_table_mag.find_all('tr')
head_mag = rasp_lines_mag[0].find_all('td')
fac_names_mag = [name.text for name in head_mag]
rasp_lines_mag[1:]
hrefs_mag = [[a['href'], a.text.split('\n')[0]] for a in rasp_lines_mag[1].find_all('a')]

# вилучаємо номер курсу та адресу excel-файла в список 'result_list'
result_list = []
for line in rasp_lines[1:]:
    href = [[a.text.split('\n')[0], a['href']] for a in line.find_all('a')]
    result_list.append(list(zip(fac_names, href)))
# робимо остаточний список
result = []
for item in result_list:
    for elem in item:
        result.append([elem[0], elem[1][0], 'https://knute.edu.ua' + elem[1][1]])

result_list_mag = []
for line in rasp_lines_mag[1:]:
    href_mag = [[a.text.split('\n')[0], a['href']] for a in line.find_all('a')]
    result_list_mag.append(list(zip(fac_names_mag, href_mag)))
# робимо остаточний список
result_mag = []
for item in result_list_mag:
    for elem in item:
        result_mag.append([elem[0], elem[1][0]+"м", 'https://knute.edu.ua' + elem[1][1]])

# завантажимо результат в датафрейм
schedule_prefinal = pd.DataFrame(result, columns=['Факультет', 'Курс', 'URL'], dtype="str")
schedule_prefinal_mag = pd.DataFrame(result_mag, columns=['Факультет', 'Курс', 'URL'], dtype="str")
result_schedule_prefinal = pd.concat([schedule_prefinal, schedule_prefinal_mag], ignore_index=True)
#print(df.head(10))
result_schedule_prefinal['URL'].values[:5]
# відсортуєм по факультету-курсу
schedule_sorted = result_schedule_prefinal.sort_values(by=['Факультет', 'Курс'])
schedule_sorted.set_index('Факультет')[:7]
schedule_sorted.to_csv('schedule.csv', index=False, encoding='utf-8-sig', sep=';',columns=['Факультет', 'Курс', 'URL'])
print(schedule_sorted.dtypes)