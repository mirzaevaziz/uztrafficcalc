"""

Calculates Internet Provider approx. traffic per day use
If you have unlim unlim then you don't need it

"""
import traceback
from datetime import date, datetime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from robobrowser import RoboBrowser
from tabulate import tabulate


class Provider:
    """
    Base class of internet providers
    """

    def __init__(self):
        self._provider_name = None
        self._budget = 0
        self._tariff_plan = None
        self._payment_date = None
        self._next_payment_date = None
        self._rest_traffic = 0
        self._all_traffic = 0
        self._future_use_traffic = 0
        self._past_used_traffic = 0
        self._dashboard_table_rows = None

        session = requests.Session()
        session.verify = False
        self.browser = RoboBrowser(session=session, history=True, parser="html.parser")

    def calc_future_use_traffic(self):
        """
        Calculates approx. traffic per day use

        :returns Approx. traffic ped day use
        """
        now = date.today()

        self._future_use_traffic = self._rest_traffic / (self._next_payment_date - now).days

    def calc_past_used_traffic(self):
        """
        Calculates approx. traffic per day used

        :returns Approx. traffic ped day used
        """

        now = date.today()

        self._past_used_traffic = (self._all_traffic - self._rest_traffic) / (now - self._payment_date).days

    def print(self):
        """
        Prints current object
        """

        print("\nПровайдер: {}".format(self._provider_name))

        print("Тарифный план: {0}\nОстаток на счетe: ${1}\nСледующее списание: {2}".format(self._tariff_plan,
                                                                                           self._budget,
                                                                                           self._next_payment_date))
        # getting limits
        print("\nЛимиты\n")

        print(tabulate(self._dashboard_table_rows[1:],
                       headers=self._dashboard_table_rows[0]))

        print("Использован в день {0:.2f} Мб".format(self._past_used_traffic))
        print("Можно использовать в день {0:.2f} Мб\n".format(self._future_use_traffic))


class Sarkor(Provider):
    """
    Sarkor Telecome internet provider class
    """

    def __init__(self):
        super(Sarkor, self).__init__()
        self._provider_name = 'Sarkor Telecom'

    def login(self, login, password):
        """
        Logins to user's private cabinet

        :param login: user provide login
        :param password: user provide password
        :return: true if login successfully passed
        """
        login_url = 'https://billing2.sarkor.uz/apex/f?p=PK:LOGIN:3375616741350930'
        self.browser.open(login_url)
        _ = self.browser.get_form(id='wwvFlowForm')
        _['p_t01'].value = login
        _['p_t02'].value = password
        self.browser.submit_form(_)

        # check whether login successfull or not
        return len(self.browser.select('#clientLogin')) > 0

    def set_values(self):
        """
        Setting all necessary values to this object

        :return: None
        """
        # getting right top values
        values = self.browser.select('.innerRight > .cVal')

        if len(values) == 0:
            raise ValueError("Couldn't find top left div with exp '.innerRight > .cVal'")

        self._budget = float(values[1].text)
        self._tariff_plan = values[0].text
        self._next_payment_date = datetime.strptime(values[2].text, "%d.%m.%Y").date()

        _ = self.browser.select('#contractRightColumn > #cLimitsTable > table > tr')

        if len(_) == 0:
            raise ValueError(
                "Couldn't find Limits table rows with exp ''#contractRightColumn > #cLimitsTable > table > tr'")

        self._dashboard_table_rows = [[r.text.replace("–", "-") for r in _[0].select('th')]]
        self._dashboard_table_rows += [[v.text.replace("–", "-") for v in r.select('td')] for r in _[1:]]

        self._rest_traffic = 0
        self._all_traffic = 0

        for row in self._dashboard_table_rows[1:]:
            self._rest_traffic = float(row[5][:-3])
            self._all_traffic += float(row[2][:-3])
            self._payment_date = datetime.strptime(row[6], "%d.%m.%Y").date()
            if row[9] == 'Нет':
                break

        self.calc_future_use_traffic()
        self.calc_past_used_traffic()


def main():
    """
    main function
    """

    requests.packages.urllib3.disable_warnings(
        InsecureRequestWarning)  # Silent InsecureRequestWarning (Switch off ssl warning)

    provider = Sarkor()
    # login
    while not provider.login(input("login: "), input("password: ")):
        print("Login or password incorrect.")

    provider.set_values()

    provider.print()


if __name__ == "__main__":

    # noinspection PyBroadException
    try:
        main()
    except:
        print(traceback.format_exc())

    input("Press Enter to exit...")
