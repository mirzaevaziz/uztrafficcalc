"""

Calculates Sarkor Internet Provider approx. traffic per day use
If you have unlim unlim then you don't need it

"""

from datetime import date, datetime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from robobrowser import RoboBrowser
from tabulate import tabulate


def calc(last_date, rest_traffic):
    """
    Calculates approx. traffic per day use
    :param last_date: Last date of this month
    :param rest_traffic: Rest traffic of this month

    :returns Approx. traffic ped day use
    """
    now = date.today()

    print('Примерный расход по днямру-2414680 = ', rest_traffic / (last_date - now).days)

    return rest_traffic / (last_date - now).days


def main():
    """
    Getting approx. traffic ped day use from Sarkor's billing web application
    Reqires login and password for enter user's cabinet

    :return: Approx. traffic ped day use from Sarkor's billing web application
    """

    session = requests.Session()
    session.verify = False

    browser = RoboBrowser(session=session, history=True, parser="html.parser")

    # login
    login_url = 'https://billing2.sarkor.uz/apex/f?p=PK:LOGIN:3375616741350930'
    browser.open(login_url)
    form = browser.get_form(id='wwvFlowForm')
    form['p_t01'].value = input("login:")
    form['p_t02'].value = input("password:")
    browser.submit_form(form)

    # getting right top values
    values = browser.select('.innerRight .cVal')

    if len(values) == 0:
        print("Login or password incorrect.")
        main()
        return

    print("\nТарифный план: {0}\nОстаток на счетe: ${1}\nСледующее списание: {2}".format(values[0].text
                                                                                         , values[1].text
                                                                                         , values[2].text))

    dt = datetime.strptime(values[2].text, "%d.%m.%Y").date()

    # getting limits
    print("\nЛимиты\n")
    rows = browser.select('#contractRightColumn > #cLimitsTable > table > tr')

    print(tabulate([[v.text.replace("–", "-") for v in r.select('td')] for r in rows[1:]],
                   headers=[r.text.replace("–", "-") for r in rows[0].select('th')]))

    rest = float(rows[1].select('td')[5].text[:-3])

    if rest == 0:
        rest = float(rows[2].select('td')[5].text[:-3])

    return calc(dt, rest)


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(
        InsecureRequestWarning)  # Silent InsecureRequestWarning (Switch off ssl warning)

    main()

    input("Press Enter to exit...")
