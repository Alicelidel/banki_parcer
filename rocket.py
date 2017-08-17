import requests
from bs4 import BeautifulSoup
import re
from get_desc import get_desc
import settings

#скачиваем страницу по url
s = requests.Session()
request = s.get(settings.BASE_URL + settings.RATING_RESOURCE)
text = request.text


#парсинг скачанной страницы
results = []
soup = BeautifulSoup(text, 'lxml')
bank_list = soup.find('table', {'class': 'standard-table standard-table--row-highlight margin-bottom-small margin-top-x-small'}).find('tbody')
items = bank_list.find_all('tr')


for item in items:

    #id
    bank_id = item.find('td', {'class': 'is-center table-title '}).text
    bank_id = re.findall(r'\s[\d]+', bank_id)

    #name
    bank_name = item.find('div').find('a', {'class': 'widget__link'}).text
    bank_name = re.findall(r'\w[\D]+\w\D', bank_name)

    #url
    bank_url = item.find('div').find('a', {'class': 'widget__link'}).get('href')

    #money
    bank_money = item.find('td',{'class': 'text-align-right'}).text
    bank_money = re.findall(r'\d[\d\s]+\d', bank_money)

    results.append({
        'bank_id': bank_id,
        'bank_name': bank_name,
        'bank_url': bank_url,
        'bank_money': bank_money
    })


#выводим результаты
print('Номер банка в рейтинге |           Финансы          |      Название банка     ')
for result in results:
    print(result['bank_id'][0],'                    |  ',result['bank_money'][0], '       | ',result['bank_name'][0])

#получаем описание каждого банка по ссылке
for bank in results:
        bank['bank_desc'] = get_desc(bank['bank_url'])
        print(bank['bank_desc'])