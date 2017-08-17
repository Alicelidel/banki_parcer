import requests
from bs4 import BeautifulSoup
import settings

def get_desc(bank_url):
    """функция получения описания банка"""
    # получаем ссылку для перехода на страницу банка
    s = requests.Session()
    desc = settings.BASE_URL + settings.RATING_RESOURCE + bank_url
    request = s.get(desc)
    text = request.text

    # получаем ссылку для перехода на описание
    soup = BeautifulSoup(text, 'lxml')
    bank_url_to_desc = soup.find('div', {'class': 'layout-columns-wrapper margin-bottom-large'}).find('div', {
        'class': 'bank-page-header'}).find('a').get('href')

    # переходим на описание и вытаскиваем его
    desc_url = settings.BASE_URL + bank_url_to_desc

    # теперь вытаскиваем описание банка по ссылке
    request = s.get(desc_url)
    text = request.text
    soup = BeautifulSoup(text, 'lxml')

    # находим ту часть страницы, в которой хранится описание. описание состоит из блоков em, которых может быть от одного и больше.
    # если же описания в этих блоках нет, значит у банка нет лицензии, что мы и прописываем далее
    bank_descs = soup.find('article', {'class': 'font-size-medium font-italic'})

    if bank_descs:
        bank_descs = bank_descs.find_all('em')
        bank_desc = ''
        for elem in bank_descs:
            bank_desc += elem.text
        # полученное описание добавляем к банку
        description = bank_desc
    else:
        # в случае отзыва лицензии
        description = 'Лицензия банка отозвана'
    # выводим описание банков
    return description