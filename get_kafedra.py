import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
#print(dir(requests))
# зчитати головну сторінку та виправити кодування (якщо необхідно)
url = 'https://knute.edu.ua/'
main_page = requests.get(url)
#print(dir(main_page))
main_page.text[:500]
main_page.encoding
main_page.apparent_encoding
main_page.encoding = main_page.apparent_encoding
#print(main_page.text[:500])
knteu_main_page = main_page.text
# розпарсити сторінку `main_page`
main_page_parsed = bs(knteu_main_page, features='html.parser')
#print(dir(main_page_parsed))
back = main_page_parsed.find('span', text='Факультети кафедри')
#print(back)
faculty_table_row = back.find_parent('a').find_parent('li').find_next('ul')
#print(faculty_table_row)
urls = []
for tag in faculty_table_row.find_all('li'):
    a_tag = tag.find('a')
    try:
        if 'href' in a_tag.attrs:
            url = a_tag.text, 'https://knute.edu.ua' + a_tag.get('href').replace(' ','%20')
            urls.append(url)
    except:
        pass

# print(urls)
df = pd.DataFrame(urls, columns=['Назва', 'URL'])
df.to_csv('kafedra.csv', index=False, encoding='utf-8-sig', sep=';',columns=['Назва', 'URL'])