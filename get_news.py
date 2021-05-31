import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# отримаємо сторінку новин 
url = 'https://knute.edu.ua/b/read-news/?uk'
resp = requests.get(url)
#print(dir(resp))
resp.text[:500]
resp.encoding
resp.apparent_encoding
resp.encoding = resp.apparent_encoding
#print(resp.text[:500])
knteu_news_page = resp.text
parsed_news = bs(knteu_news_page, features='html.parser')
#print(dir(parsed_news))
back = parsed_news.find('h3', text='Новини')
#print(back)
news_table_row = back.findNextSibling('div', {"class": "pull-left"})
#print(news_table_row)
urls = []
for tag in news_table_row.find_all('div', "nnews_item"):
    a = tag.find('a')
    span_tag = a.find('span').get_text()
    date_tag = a.find('small').get_text()
    if 'href' in a.attrs:
        url = date_tag, span_tag, 'https://knute.edu.ua' + a.attrs['href']
        urls.append(url)
#print(urls)
# завантажимо результат в датафрейм
df = pd.DataFrame(urls, columns=['Дата', 'Анонс', 'URL'])
df.to_csv('news.csv', index=False, encoding='utf-8-sig', sep=';',columns=['Дата', 'Анонс', 'URL'])