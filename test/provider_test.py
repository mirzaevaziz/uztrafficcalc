from datetime import date, timedelta

from uz_inet_traffic_calc.providers.Provider import Provider


def test_provider_calc_future_use_traffic():
    provider = Provider()
    if provider.future_use_traffic > 0:
        raise ValueError('future_use_traffic > 0 after __init___')
    if provider.rest_traffic > 0:
        raise ValueError('rest_traffic > 0 after __init___')
    if provider.next_payment_date is not None:
        raise ValueError('next_payment_date is not None  after __init___')

    provider._rest_traffic = 1000
    provider._next_payment_date = date.today() + timedelta(days=2)
    provider.calc_future_use_traffic()
    if provider.future_use_traffic == 0:
        raise ValueError('calc_future_use_traffic() is not working')


def test_provider_calc_future_use_traffic():
    provider = Provider()
    if provider.past_used_traffic > 0:
        raise ValueError('past_used_traffic > 0 after __init___')
    if provider.rest_traffic > 0:
        raise ValueError('rest_traffic > 0 after __init___')
    if provider.all_traffic > 0:
        raise ValueError('all_traffic > 0 after __init___')
    if provider.payment_date is not None:
        raise ValueError('payment_date is not None  after __init___')

    provider._all_traffic = 2000
    provider._rest_traffic = 1000
    provider._payment_date = date.today() + timedelta(days=-2)
    provider.calc_past_used_traffic()
    if provider.past_used_traffic == 0:
        raise ValueError('calc_future_use_traffic() is not working')
