import matplotlib.pyplot as plt
import plotly.offline as ply
import plotly.figure_factory as ff
import json


def make_plot(x,y,color):
    """построение графика по заданным х и у"""
    plt.title('Финансовые показатели')
    plt.xlabel('Месяц, номер')
    plt.ylabel('Активы, млрд.руб.')

    return plt.plot(x, y, color=color)


def make_json(banks):
    """функция, которая представляет данные в формате json"""

    temp_doc = json.dumps(banks, sort_keys=True, indent=4, separators=(',', ' : '))

    return temp_doc


def make_table(banki):
    """построение таблицы с финансовыми показателями - 50 банков, номер, название, активы"""

    data_set = [['Номер','Банк','Активы']]
    for bank in banki:
        data_set.append([bank['bank_id'], bank['bank_name'], bank['bank_money'] ])

    table = ff.create_table(data_set, height_constant=20)
    ply.plot(table, filename='banki.html')
    return data_set
