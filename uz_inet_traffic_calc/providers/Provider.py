from datetime import date

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

    @property
    def future_use_traffic(self):
        return self._future_use_traffic

    @property
    def rest_traffic(self):
        return self._rest_traffic

    @property
    def next_payment_date(self):
        return self._next_payment_date

    @property
    def past_used_traffic(self):
        return self._past_used_traffic

    @property
    def all_traffic(self):
        return self._all_traffic

    @property
    def payment_date(self):
        return self._payment_date
