import requests
from bs4 import BeautifulSoup
import re


#скачиваем страницу по url
s = requests.Session()
url = 'http://www.banki.ru/banks/ratings/'
request = s.get(url)
text = request.text
#print(text)


#парсинг скачанной страницы
results = []
soup = BeautifulSoup(text, 'lxml')
bank_list = soup.find('table', {'class': 'standard-table standard-table--row-highlight margin-bottom-small margin-top-x-small'}).find('tbody')
items = bank_list.find_all('tr')

for item in items:

    #id
    bank_id = item.find('td', {'class': 'is-center table-title '}).text
    bank_id = re.findall(r'\s[\d]+', bank_id)
    #print(bank_id)

    #name
    bank_name = item.find('div').find('a', {'class': 'widget__link'}).text
    bank_name = re.findall(r'\w[\D]+\w\D', bank_name)
    #print(bank_name)

    #url
    bank_url = item.find('div').find('a', {'class': 'widget__link'}).get('href')

    #money
    bank_money = item.find('td',{'class': 'text-align-right'}).text
    bank_money = re.findall(r'\d[\d\s]+\d', bank_money)
    #print(bank_money)

    results.append({
        'bank_id': bank_id,
        'bank_name': bank_name,
        'bank_url': bank_url,
        'bank_money': bank_money
    })


#выводим результаты
print('Номер банка в рейтинге |           Финансы          |      Название банка     ')
for result in results:
    print(result['bank_id'],'                |  ',result['bank_money'], '     | ',result['bank_name'])

#получаем описание каждого банка по ссылке
for bank in results:

    #получаем ссылку для перехода на страницу банка
    desc = url + bank['bank_url']
    request = s.get(desc)
    text = request.text

    #получаем ссылку для перехода на описание
    soup = BeautifulSoup(text, 'lxml')
    bank_url_to_desc = soup.find('div', {'class':'layout-columns-wrapper margin-bottom-large'}).find('div', {'class':'bank-page-header'}).find('a').get('href')

    #переходим на описание и вытаскиваем его
    #ссылка на описание банка лежит на том же url, но от исходного url надо убрать лишнее, оставив только www.banki.ru
    desc_url = url[:-15] + bank_url_to_desc

    #теперь вытаскиваем описание банка по ссылке
    request = s.get(desc_url)
    text = request.text
    soup = BeautifulSoup(text, 'lxml')

    #находим ту часть страницы, в которой хранится описание. описание состоит из блоков em, которых может быть от одного и больше.
    #если же описания в этих блоках нет, значит у банка нет лицензии, что мы и прописываем далее
    bank_descs = soup.find('article', {'class':'font-size-medium font-italic'})

    if bank_descs:
        bank_descs = bank_descs.find_all('em')
        bank_desc = ''
        for elem in bank_descs:
            bank_desc += elem.text
        #полученное описание добавляем к банку
        bank['bank_desc'] = bank_desc
    else:
        #в случае отзыва лицензии
        bank['bank_desc'] = 'Лицензия банка отозвана'
    #выводим описание банков
    print(bank['bank_desc'])