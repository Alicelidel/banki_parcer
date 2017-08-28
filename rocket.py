import requests
from get_info import get_desc, get_money, get_json, get_xy_for_bank, get_data, get_bank_list
import settings
from make_info import make_plot, make_json, make_table


def main():
    s = requests.Session()
    text = s.get(settings.BASE_URL + settings.RATING_RESOURCE).text
    results = get_data(text)

    print('Таблица с финансовыми показателями первых 50 банков в рейтинге.\n')
    make_table(results)

    print('\nИнформация о всех 50 банках из рейтинга:\n')
    for bank in results:
            bank['bank_desc'] = get_desc(bank['bank_url'])
            print(bank['bank_id'], bank['bank_desc'])

    temp_doc = make_json(results)

    #посчитаем финансы какого-то одного банка за полгода и построим график - выбираем лидера
    #для этого необходимо перейти на страничку банка - нужно узнать hidden_id
    bank_id = 1
    hidden_id = results[bank_id-1]['bank_hidden_id']
    print('Выводим финансовые показатели банка ',results[bank_id-1]['bank_name'])
    x,y = get_xy_for_bank(hidden_id)
    line_color = 'g' #выберем цвет линии
    plt = make_plot(x,y,line_color)
    plt.show()

    #теперь построим график с фин. показателями топ 10 банков
    colors = ['g','r','b','k','y','m','c','g','r','b']
    for bank in results[:10]:
        color = colors.pop(0)
        hidden_id = bank['bank_hidden_id']
        x,y = get_xy_for_bank(hidden_id)
        plt = make_plot(x,y,color)
    plt.show()

    get_json(temp_doc)


if __name__ == '__main__':
    main()