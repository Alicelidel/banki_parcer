import requests, re
from bs4 import BeautifulSoup
import settings
import json
from pprint import pprint
from datetime import date, timedelta
from time import strftime

def get_desc(bank_url):
    """функция получения описания банка"""
    s = requests.Session()
    desc = settings.BASE_URL + settings.RATING_RESOURCE + bank_url
    request = s.get(desc)
    text = request.text

    soup = BeautifulSoup(text, 'lxml')
    bank_url_to_desc = soup.find('div', {'class': 'layout-columns-wrapper margin-bottom-large'}).find('div', {
        'class': 'bank-page-header'}).find('a').get('href')

    desc_url = settings.BASE_URL + bank_url_to_desc
    request = s.get(desc_url)
    text = request.text
    description = parse_desc(text)

    return description

def parse_desc(text):
        """ находим ту часть страницы, в которой хранится описание. описание состоит из блоков em, которых может быть от одного и больше."""
        soup = BeautifulSoup(text, 'lxml')
        bank_descs = soup.find('article', {'class': 'font-size-medium font-italic'})

        if bank_descs:
            bank_descs = bank_descs.find_all('em')
            bank_desc = ''
            for elem in bank_descs:
                bank_desc += elem.text
            description = bank_desc
        else:
            description = 'Лицензия банка отозвана'

        return description


def get_money(prev_month, curr_month, bank_hidden_id):
    """функция, которая возвращает финансы за период с второго указанного месяца по первый
    на сайте конкретно с первого числа месяца до первого числа, т.е деньги за полный второй месяц
    т.е финансы за второй месяц - curr_month"""
    s = requests.Session()
    date_url = '&date1=2017-{}-01&date2=2017-{}-01'.format(curr_month, prev_month)
    money_url = settings.BASE_URL + settings.RATING_RESOURCE + bank_hidden_id + date_url
    text = s.get(money_url).text
    soup = BeautifulSoup(text, 'lxml')
    money = soup.find('body',{'class':'modern-design'}).find('div',{'class':'widget'}).find('tbody').find('tr').find('td',{'class':'text-align-right'}).text
    money = money.replace(' ', '')

    #значение дано в тыс.рублей, поэтому мы ещё сократим число до количества миллиардов, чтобы представление было более удобным
    money = int(money[:-6])

    return money


def get_json(temp_doc):
    """функция, которая достаёт данные из json"""
    data = json.loads(temp_doc)

    pprint(data, depth=2, width=50)


def get_xy_for_bank(hidden_id):
    """функция считает месяца и активы для выбранного банка"""
    one_month = timedelta(days=30)

    #значения по х - месяца, последние полгода
    x = []
    for i in range(1,7):
        month = (date.today() - one_month * i).month
        x.append(month)

    #значения по у (активы):
    y = []
    for i in range(7, 1, -1):
        curr_month = (date.today() - one_month * i)
        curr_month = strftime('%m', curr_month.timetuple())
        prev_month = (date.today() - one_month * (i - 1))
        prev_month = strftime('%m', prev_month.timetuple())

        money = get_money(prev_month, curr_month, hidden_id)
        y.append(money)

    return x,y


def get_data(text):
    """функция которая парсит блок каждого банка и возвращает данные"""
    results = []
    soup = BeautifulSoup(text, 'lxml')
    bank_list = get_bank_list(soup)
    items = bank_list.find_all('tr')

    for item in items:
        bank_id = item.find('td', {'class': 'is-center table-title '}).text
        bank_id = re.match(r'\s+(\d+)\s+', bank_id).group(1)

        bank_name = item.find('div').find('a', {'class': 'widget__link'}).text
        bank_name = re.match(r'\s+(\S.+\S)\s', bank_name).group(1)

        bank_url = item.find('div').find('a', {'class': 'widget__link'}).get('href')

        bank_hidden_id = re.match(r'.*(\?BANK_ID=[\d]+).*', bank_url).group(1)

        bank_money = item.find('td', {'class': 'text-align-right'}).text
        bank_money = re.match(r'\s+([\d[\d\s]+\d)\s+', bank_money).group(1)

        results.append({
            'bank_id': bank_id,
            'bank_name': bank_name,
            'bank_url': bank_url,
            'bank_hidden_id': bank_hidden_id,
            'bank_money': bank_money
        })
        print(results)

    return results


def get_bank_list(soup):
    bank_list = soup.find('table', {'class': 'standard-table standard-table--row-highlight margin-bottom-small margin-top-x-small'}).find('tbody')
    return bank_list