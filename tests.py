import unittest
from unittest import mock
from get_info import get_money, parse_desc, get_data
from make_info import make_plot, make_table
import numpy as np




class TestParseDesc(unittest.TestCase):

    def testParseDesc(self):
        with open('docs_for_tests/parse_desc_sber.html', 'rb') as file:
            html = file.read()
        original_text = 'ПАО «Сбербанк России» — крупнейший банк в России и СНГ с самой широкой сетью подразделений, предлагающий весь спектр инвестиционно-банковских услуг. Учредителем и основным акционером Сбербанка является Центральный банк РФ, владеющий 50% уставного капитала плюс одной голосующей акцией; свыше 40% акций принадлежит зарубежным компаниям. Около половины российского рынка частных вкладов, а также каждый третий корпоративный и розничный кредит в России приходятся на Сбербанк.'
        self.assertTrue(parse_desc(html) == original_text)


class TestGetMoney(unittest.TestCase):

    @mock.patch('requests.session')
    def testGetMoney(self, session):
        with open('docs_for_tests/get_money_sber.html', 'rb') as file:
            html = file.read()
        session().get.return_value = html
        self.assertTrue(get_money('06','07','?BANK_ID=322') == 22864)
        self.assertRaises(expected_exception=AttributeError, prev_month='07',curr_month='08',bank_hidden_id='?BANK_ID=1')


class TestGetData(unittest.TestCase):

    def testGetData(self):
        with open('docs_for_tests/get_data_sber.html', 'rb') as file:
            html = file.read()
        original_data = [{'bank_id': '1', 'bank_name': 'Сбербанк России', 'bank_url': '?BANK_ID=322&date1=2017-08-01&date2=2017-07-01', 'bank_hidden_id': '?BANK_ID=322', 'bank_money': '23 322 666 077'}]
        self.assertTrue(get_data(html) == original_data)


class TestMakePlot(unittest.TestCase):

    def testMakePlot(self):
        #сравнивает данные которые передаются графику с данными которые должны быть
        xvals = [0,1,2]
        yvals = [0,1,2]
        line = make_plot(xvals, yvals, 'g')
        y_plot = line[0].get_ydata()
        np.testing.assert_array_equal(y_plot, yvals)




class TestMakeTable(unittest.TestCase):

    def testMakeTable(self):
        original_data = [{'bank_id': '1', 'bank_name': 'Сбербанк России',
                          'bank_url': '?BANK_ID=322&date1=2017-08-01&date2=2017-07-01',
                          'bank_hidden_id': '?BANK_ID=322', 'bank_money': '23 322 666 077'}]
        #проверим, имеется ли на выходе тот список, который должен быть для построения таблицы
        result = make_table(original_data)
        need_to_be = [['Номер','Банк','Активы'],['1','Сбербанк России','23 322 666 077']]
        self.assertListEqual(result, need_to_be)


if __name__ == '__main__':
    unittest.main()