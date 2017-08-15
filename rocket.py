import requests
from bs4 import BeautifulSoup
import re


#скачиваем страницу по url
s = requests.Session()
s.headers.update({
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
})
url = 'http://www.banki.ru/banks/ratings/'
request = s.get(url)
with open('test.html','wb') as output_file:
    output_file.write(request.text.encode('cp1251'))


#парсинг скачанной страницы
text = open('test.html',mode='r')
results = []

soup = BeautifulSoup(text)
bank_list = soup.find('table', {'class': 'standard-table standard-table--row-highlight margin-bottom-small margin-top-x-small'}).find('tbody')
items = bank_list.find_all('tr')
#print(items[0])
for item in items:

    #id
    bank_id = item.find('td', {'class': 'is-center table-title '}).text
    bank_id = re.findall(r'\s[\d]+', bank_id)
    #print(bank_id)

    #http
    bank_http = item.find('div').find('a', {'class': 'widget__link'}).get('href')
    #print(bank_http)

    #get description

    #name
    bank_name = item.find('div').find('a', {'class': 'widget__link'}).text
    bank_name = re.findall(r'\w[\D]+\w\D', bank_name)
    #print(bank_name)

    #money
    bank_money = item.find('td',{'class': 'text-align-right'}).text
    bank_money = re.findall(r'\d[\d\s]+\d', bank_money)
    #print(bank_money)

    results.append({
        'bank_id': bank_id,
        'bank_http': bank_http,
        'bank_name': bank_name,
        'bank_money': bank_money
    })


#выводим результаты
print('Номер банка в рейтинге |           Финансы          |      Название банка     ')
for result in results:
    print(result['bank_id'],'                |  ',result['bank_money'], '     | ',result['bank_name'])
