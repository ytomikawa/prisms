import os
import pandas
import time
import logging
import math

from datetime import datetime
from bulk_update.helper import bulk_update

from django.shortcuts import render
from django.conf import settings
from .models import SecurityCode, Security, SecurityPrice, SecurityMargin

from django.http import HttpResponse

def index(request):
    before = datetime.now()
    #importSecurities()
    after = datetime.now()
    delta = after - before
    print(delta.total_seconds())
    #codes = SecurityCode.objects.all()
    #for c in codes:
    #    print(c.code)
    return HttpResponse("Hello, world. You're at the polls index.")


def import_data(request, target, parameter = ''):
    logging.info('importing started: target=' + target + ', parameter=' + parameter)
    before = datetime.now()
    if target == 'security':
        import_securities(parameter)
    elif target == 'edinet_code':
        import_edinet_code(parameter)
    elif target == 'listed_date':
        import_listed_date(parameter)
    elif target == 'price':
        import_price(parameter)
    elif target == 'margin':
        import_margin(parameter)
    else:
        # Undefined target
        raise ValueError('Undefined target:' + target)
    after = datetime.now()
    seconds = str((after - before).total_seconds())

    message = 'importing completed: target=' + target + ', parameter=' + parameter +' (' + seconds + 'sec)'
    logging.info(message)
    return HttpResponse(message)


def import_margin(parameter):
    csv_path = os.path.join(settings.KABUPLUS_DIRECTORY, 'jsf-balance-data', 'daily', 'jsf-balance-data.csv')
    created = datetime(*time.localtime(os.path.getctime(csv_path))[:3])
    updated_security_margins = []
    security_codes = {c.code : c for c in SecurityCode.objects.all()}

    dataset = pandas.read_csv(csv_path, encoding="shift_jis")
    for index, row in dataset.iterrows():
        code = str(row[0])
        market = str(row[2])
        jsf_margin_type = str(row[5])
        jsf_buy_new = parse_integer(row[6])
        jsf_buy_refund = parse_integer(row[7])
        jsf_buy_balance = parse_integer(row[8])
        jsf_sell_new = parse_integer(row[9])
        jsf_sell_refund = parse_integer(row[10])
        jsf_sell_balance = parse_integer(row[11])
        jsf_net_balance = parse_integer(row[12])
        jsf_net_change = parse_integer(row[13])

        # 東証以外(名証など)のデータは必要ないので読み捨てる
        if market != u'東証':
            continue

        security_code = security_codes.get(code)
        if security_code is None:
            logging.warning('SecurityCode is not exist: code=' + code)
            continue

        try:
            security_margin = SecurityMargin.objects.get(security_code__code=code, date=created)
            security_margin.jsf_margin_type = jsf_margin_type
            security_margin.jsf_buy_new = jsf_buy_new
            security_margin.jsf_buy_refund = jsf_buy_refund
            security_margin.jsf_buy_balance = jsf_buy_balance
            security_margin.jsf_sell_new = jsf_sell_new
            security_margin.jsf_sell_refund = jsf_sell_refund
            security_margin.jsf_sell_balance = jsf_sell_balance
            security_margin.jsf_net_balance = jsf_net_balance
            security_margin.jsf_net_change = jsf_net_change
            updated_security_margins.append(security_margin)
        except SecurityMargin.DoesNotExist:
            security_code = security_codes.get(code)
            security_margin = SecurityMargin(
                security_code=security_code,
                date=created,
                jsf_margin_type=jsf_margin_type,
                jsf_buy_new=jsf_buy_new,
                jsf_buy_refund=jsf_buy_refund,
                jsf_buy_balance=jsf_buy_balance,
                jsf_sell_new=jsf_sell_new,
                jsf_sell_refund=jsf_sell_refund,
                jsf_sell_balance=jsf_sell_balance,
                jsf_net_balance=jsf_net_balance,
                jsf_net_change=jsf_net_change,
            )
            security_margin.security_code.save()
            security_margin.save()
    bulk_update(updated_security_margins)


def import_price(parameter):
    csv_path = os.path.join(settings.KABUPLUS_DIRECTORY, 'japan-all-stock-prices-2', 'daily', 'japan-all-stock-prices-2.csv')
    created = datetime(*time.localtime(os.path.getctime(csv_path))[:3])
    updated_security_prices = []
    security_codes = {c.code : c for c in SecurityCode.objects.all()}

    dataset = pandas.read_csv(csv_path, encoding="shift_jis")
    for index, row in dataset.iterrows():
        code = str(row[0])
        opening_price = parse_float(row[9])
        max_price = parse_float(row[10])
        min_price = parse_float(row[11])
        closing_price = parse_float(row[6])
        change = parse_float(row[7])
        change_ratio = parse_float(row[8])
        vwap = parse_float(row[12])
        trading_volume = parse_float(row[13])
        trading_volume_ratio = parse_float(row[14])
        trading_value = parse_float(row[15])
        annual_max_price = parse_float(row[20])
        annual_max_price_deviation_ratio = parse_float(row[21])
        annual_min_price = parse_float(row[23])
        annual_min_price_deviation_ratio = parse_float(row[24])

        security_code = security_codes.get(code)
        if security_code is None:
            logging.warning('SecurityCode is not exist: code=' + code)
            continue

        try:
            security_price = SecurityPrice.objects.get(security_code__code=code, date=created)
            security_price.opening_price = opening_price
            security_price.max_price = max_price
            security_price.min_price = min_price
            security_price.closing_price = closing_price
            security_price.change = change
            security_price.change_ratio = change_ratio
            security_price.vwap = vwap
            security_price.trading_volume = trading_volume
            security_price.trading_volume_ratio = trading_volume_ratio
            security_price.trading_value = trading_value
            security_price.annual_max_price = annual_max_price
            security_price.annual_max_price_deviation_ratio = annual_max_price_deviation_ratio
            security_price.annual_min_price = annual_min_price
            security_price.annual_min_price_deviation_ratio = annual_min_price_deviation_ratio
            updated_security_prices.append(security_price)
        except SecurityPrice.DoesNotExist:
            security_code = security_codes.get(code)
            security_price = SecurityPrice(
                security_code=security_code,
                date=created,
                opening_price=opening_price,
                max_price=max_price,
                min_price=min_price,
                closing_price=closing_price,
                change=change,
                change_ratio=change_ratio,
                vwap=vwap,
                trading_volume=trading_volume,
                trading_volume_ratio=trading_volume_ratio,
                trading_value=trading_value,
                annual_max_price=annual_max_price,
                annual_max_price_deviation_ratio=annual_max_price_deviation_ratio,
                annual_min_price=annual_min_price,
                annual_min_price_deviation_ratio=annual_min_price_deviation_ratio,
            )
            security_price.security_code.save()
            security_price.save()
    bulk_update(updated_security_prices)


def import_edinet_code(parameter):
    security_codes = {c.code : c for c in SecurityCode.objects.all()}
    updated_security_codes = []

    csv_path = os.path.join('data', 'EdinetcodeDlInfo.csv')
    dataset = pandas.read_csv(csv_path, encoding="Shift_JISx0213", skiprows=1)

    for index, row in dataset.iterrows():
        edinet_code = str(row[0])
        code = str(row[11])
        if len(code) >= 5:
            code = code[0:4] # 4桁の証券コードにする

        security_code = security_codes.get(code)
        if security_code is not None:
            security_code.edinet_code = edinet_code
            updated_security_codes.append(security_code)

    bulk_update(updated_security_codes)


def import_listed_date(parameter):
    security_codes = {c.code : c for c in SecurityCode.objects.all()}
    updated_security_codes = []

    csv_path = os.path.join(settings.KABUPLUS_DIRECTORY, 'japan-all-stock-information', 'monthly', 'listing-date.csv')
    dataset = pandas.read_csv(csv_path, encoding="shift_jis", skiprows=1)

    for index, row in dataset.iterrows():
        code = str(row[0])
        listed_date = parse_date(row[1]) # 'YYYY/MM'のように月までしか入力がないため、日付を固定で足す

        security_code = security_codes.get(code)
        if security_code is not None:
            security_code.listed_date = listed_date
            updated_security_codes.append(security_code)

    bulk_update(updated_security_codes)


def import_securities(parameter):
    csv_path = os.path.join(settings.KABUPLUS_DIRECTORY, 'japan-all-stock-data', 'daily', 'japan-all-stock-data.csv')
    created = datetime(*time.localtime(os.path.getctime(csv_path))[:3])

    updated_security_codes = []
    updated_securities = []

    security_codes = {c.code : c for c in SecurityCode.objects.all()}
    #securities = {s.security_code.code : s for s in Security.objects.filter(date=created)}

    dataset = pandas.read_csv(csv_path, encoding="shift_jis")
    for index, row in dataset.iterrows():
        code = str(row[0])
        name = str(row[1])
        market = str(row[2])
        business = str(row[3])
        market_value = parse_float(row[4])
        shares_number = parse_float(row[5])
        dividend = parse_float(row[7])
        per = parse_float(row[8])
        pbr = parse_float(row[9])
        eps = parse_float(row[10])
        bps = parse_float(row[11])
        unit_size = parse_float(row[13])

        security_code = security_codes.get(code)
        if security_code is None:
            security_code = SecurityCode(code=code, display_name=name)
            security_code.save()
            security_codes[code] = security_code
        else:
            security_code.display_name = name
            updated_security_codes.append(security_code)

        #security = securities.get(security_code)
        try:
            security = Security.objects.get(security_code__code=code, date=created)
            security.name = name
            security.market = market
            security.business = business
            security.market_value = market_value
            security.shares_number = shares_number
            security.dividend = dividend
            security.per = per
            security.pbr = pbr
            security.eps = eps
            security.bps = bps
            security.unit_size = unit_size
            updated_securities.append(security)
        except Security.DoesNotExist:
            security_code = security_codes.get(code)
            security = Security(
                security_code=security_code,
                date=created,
                name=name,
                market=market,
                business=business,
                market_value=market_value,
                shares_number=shares_number,
                dividend=dividend,
                per=per,
                pbr=pbr,
                eps=eps,
                bps=bps,
                unit_size=unit_size
            )
            security.security_code.save()
            security.save()
    bulk_update(updated_security_codes)
    bulk_update(updated_securities)


def parse_integer(value):
    if math.isnan(value):
        return None
    elif value == '-':
        return 0
    else:
        return int(value)

def parse_float(value):
    if value == '-':
        return 0.0
    else:
        return float(value)


def parse_date(value):
    if len(value) == 7:
        date = value + '/01' # 'YYYY/MM'のように月までしか入力がないため、日付を固定で足す
        return datetime.strptime(date, '%Y/%m/%d')
    else:
        return None
