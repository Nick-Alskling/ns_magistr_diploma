import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# отримаємо сторінку новин 
url = 'https://knute.edu.ua/blog/read/?pid=16857&uk'
resp = requests.get(url)
#print(dir(resp))
resp.text[:500]
resp.encoding
resp.apparent_encoding
resp.encoding = resp.apparent_encoding
#print(resp.text[:500])
knteu_contact_page = resp.text
parsed_contacts = bs(knteu_contact_page, features='html.parser')
#print(dir(parsed_news))

amount_rows = parsed_contacts.find_all('table')[0].tbody.find_all('tr')
# print(len(amount_rows))

for i in amount_rows:
    name_column = [row.find_all('td')[0].text.strip().replace("\n", " ").replace("\xa0", " ") for row in amount_rows]
    phone_column = [row.find_all('td')[1].text.strip().replace("\n", " ").replace("\xa0", " ") for row in amount_rows]
    email_column = [row.find_all('td')[2].text.strip().replace("\n", " ").replace("\xa0", " ") for row in amount_rows]

contacts = []
for i in range(len(amount_rows)):
    contact = name_column[i], phone_column[i], email_column[i]
    contacts.append(contact)
# print(contacts)

# завантажимо результат в датафрейм
contacts_df = pd.DataFrame(contacts, columns=['Відділ', 'Телефон', 'email'])
contacts_df.to_csv('contacts.csv', index=False, encoding='utf-8-sig', sep=';',columns=['Відділ', 'Телефон', 'email'])