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
<<<<<<< HEAD
=======
# knteu_announces_page = resp.text
>>>>>>> 8cbd64f (latest version)
knteu_news_page = resp.text
parsed_news = bs(knteu_news_page, features='html.parser')
#print(dir(parsed_news))
back = parsed_news.find('h3', text='Новини')
<<<<<<< HEAD
#print(back)
news_table_row = back.findNextSibling('div', {"class": "pull-left"})
=======
# print(back)
news_table_row = back.find_next_sibling('div', {"class": "pull-left"})
>>>>>>> 8cbd64f (latest version)
#print(news_table_row)
urls = []
for tag in news_table_row.find_all('div', "nnews_item"):
    a = tag.find('a')
    span_tag = a.find('span').get_text()
    date_tag = a.find('small').get_text()
    if 'href' in a.attrs:
        url = date_tag, span_tag, 'https://knute.edu.ua' + a.attrs['href']
        urls.append(url)
<<<<<<< HEAD
# print(urls)
# завантажимо результат в датафрейм
df = pd.DataFrame(urls, columns=['Дата', 'Новина', 'URL'])
=======
print(urls)
# завантажимо результат в датафрейм
df = pd.DataFrame(urls, columns=['Дата', 'Новина', 'URL'])
print(df)
>>>>>>> 8cbd64f (latest version)
df.to_csv('news.csv', index=False, encoding='utf-8-sig', sep=';',columns=['Дата', 'Новина', 'URL'])


# отримаємо сторінку анонсів 
url = 'https://knute.edu.ua/b/read-allnnoun/?uk'
resp = requests.get(url)
#print(dir(resp))
resp.text[:500]
resp.encoding
resp.apparent_encoding
resp.encoding = resp.apparent_encoding
#print(resp.text[:500])
knteu_announces_page = resp.text
parsed_announces = bs(knteu_announces_page, features='html.parser')
#print(dir(parsed_news))
back_announces = parsed_announces.find('h1', text='Анонси')
# print(back_announces)

announces_table_row = back_announces.find_next("div")
# print(announces_table_row)

urls = []
class_table = announces_table_row.find_all('div', {"class": "an_item row"})
# print(class_table)

for i in range(len(class_table)):
    
    links = [link.find('a').get('href') for link in class_table]
    # print(links)

    date_tag = [date.find("span", {"class":"announ_date_digit"}).text for date in class_table]
    # print(date_tag)

    month_tag = [month.find("span", {"class":"announ_date_month"}).text for month in class_table]
    # print(month_tag)

    header_tag = [header.find("span", {"class":"thin-header"}).text for header in class_table]
    # print(header_tag)

    desc_tag = [desc.find("small", {"class":"muted"}).text for desc in class_table]
    # print(desc_tag)
    url = date_tag[i] + " " + month_tag[i], header_tag[i], desc_tag[i], 'https://knute.edu.ua' + links[i]
    urls.append(url)

# print(urls)

# завантажимо результат в датафрейм
df = pd.DataFrame(urls, columns=['Дата', "Заголовок", 'Анонс', 'URL'])
<<<<<<< HEAD
df.to_csv('announces.csv', index=False, encoding='utf-8-sig', sep=';', columns=['Дата', "Заголовок", 'Анонс', 'URL'])
=======
df.to_csv('announces.csv', index=False, encoding='utf-8-sig', sep=';', columns=['Дата', "Заголовок", 'Анонс', 'URL'])
>>>>>>> 8cbd64f (latest version)
