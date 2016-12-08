from datetime import date, datetime

from requests import Session
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

    print('Approx. traffic per day = ', rest_traffic / (last_date - now).days)

    return rest_traffic / (last_date - now).days


def main():
    session = Session()
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

    print("Plan: {0}\nMoney: {1}\nNext Date: {2}".format(values[0].text, values[1].text, values[2].text))

    dt = datetime.strptime(values[2].text, "%d.%m.%Y").date()

    # getting limits
    print("\nLimits\n")
    rows = browser.select('#contractRightColumn > #cLimitsTable > table > tr')

    print(tabulate([[v.text.replace("–", "-")for v in r.select('td')] for r in rows[1:]],
                   headers=[r.text.replace("–", "-") for r in rows[0].select('th')]))

    rest = float(rows[1].select('td')[5].text[:-3])

    if rest == 0:
        rest = float(rows[2].select('td')[5].text[:-3])

    calc(dt, rest)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
