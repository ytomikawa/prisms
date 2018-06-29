from django.db import models

class SecurityCode(models.Model):
    class Meta:
        verbose_name = u'銘柄コード'
        verbose_name_plural = u'銘柄コード'

    code = models.CharField(u'証券コード', max_length=4, unique=True, db_index=True)
    isin_code = models.CharField(u'ISINコード', max_length=12)
    edinet_code = models.CharField(u'EDINETコード', max_length=6, db_index=True)
    listed_date = models.DateField(u'上場日', null=True)
    delisted_date = models.DateField(u'上場廃止日', null=True)
    display_name = models.CharField(u'画面表示用銘柄名', max_length=1024)

    def __str__(self):
        return  self.display_name + ' (' + self.code +')'


class Security(models.Model):
    class Meta:
        verbose_name = u'銘柄'
        verbose_name_plural = u'銘柄'
        index_together = [
            ['security_code', 'date']
        ]

    security_code = models.ForeignKey(SecurityCode, on_delete=models.CASCADE)
    date = models.DateField(u'日付', null=True, db_index=True)
    name = models.CharField(u'銘柄名', max_length=1024)
    market = models.CharField(u'市場', max_length=1024)
    business = models.CharField(u'業種', max_length=1024)
    market_value = models.BigIntegerField(u'時価総額(百万円)')
    shares_number = models.BigIntegerField(u'発行済株式数')
    dividend = models.FloatField(u'1株配当')
    per = models.FloatField(u'PER')
    pbr = models.FloatField(u'PBR')
    eps = models.FloatField(u'EPS')
    bps = models.FloatField(u'BPS')
    unit_size = models.IntegerField(u'単元数')

    def __str__(self):
        return str(self.security_code) + ' ' + self.date.strftime('%Y/%m/%d')


class SecurityMargin(models.Model):
    class Meta:
        verbose_name = u'信用情報'
        verbose_name_plural = u'信用情報'
        index_together = [
            ['security_code', 'date']
        ]

    security_code = models.ForeignKey(SecurityCode, on_delete=models.CASCADE)
    date = models.DateField(u'日付', null=True, db_index=True)
    # 日証金
    jsf_margin_type = models.CharField(u'速報/確報', max_length=4)
    jsf_buy_new = models.BigIntegerField(u'融資新規', null=True)
    jsf_buy_refund = models.BigIntegerField(u'融資返済', null=True)
    jsf_buy_balance = models.BigIntegerField(u'融資残高', null=True)
    jsf_sell_new = models.BigIntegerField(u'貸株新規', null=True)
    jsf_sell_refund = models.BigIntegerField(u'貸株返済', null=True)
    jsf_sell_balance = models.BigIntegerField(u'貸株残高', null=True)
    jsf_net_balance =  models.BigIntegerField(u'差引残高', null=True)
    jsf_net_change =  models.BigIntegerField(u'差引前日比', null=True)
    jsf_max_backwardation = models.FloatField(u'最高料率', null=True)
    jsf_backwardation = models.FloatField(u'品貸料率', null=True)
    jsf_backwardation_ratio = models.FloatField(u'品貸料率(%)', null=True)
    jsf_backwardation_days = models.FloatField(u'品貸日数', null=True)
    jsf_limitation = models.CharField(u'規制', max_length=4, null=True)
    # 東証
    tse_buy_balance = models.BigIntegerField(u'信用買残高', null=True)
    tse_buy_change = models.BigIntegerField(u'信用買残高(前週比)', null=True)
    tse_sell_balance = models.BigIntegerField(u'信用売残高', null=True)
    tse_sell_change = models.BigIntegerField(u'信用売残高(前週比)', null=True)

    def __str__(self):
        return str(self.security_code) + ' ' + self.date.strftime('%Y/%m/%d')


class SecurityPrice(models.Model):
    class Meta:
        verbose_name = u'株価'
        verbose_name_plural = u'株価'
        index_together = [
            ['security_code', 'date']
        ]

    security_code = models.ForeignKey(SecurityCode, on_delete=models.CASCADE)
    date = models.DateField(u'日付', null=True, db_index=True)
    opening_price = models.FloatField(u'始値', null=True)
    max_price = models.FloatField(u'高値', null=True)
    min_price = models.FloatField(u'安値', null=True)
    closing_price = models.FloatField(u'終値', null=True)
    change = models.FloatField(u'前日比', null=True)
    change_ratio = models.FloatField(u'前日比(%)', null=True)
    vwap = models.FloatField(u'VWAP')
    trading_volume = models.BigIntegerField(u'出来高', null=True)
    trading_volume_ratio = models.FloatField(u'出来高率')
    trading_value = models.FloatField(u'売買代金(千円)')
    annual_max_price = models.FloatField(u'年初来高値')
    annual_max_price_deviation_ratio = models.FloatField(u'年初来高値乖離率')
    annual_min_price = models.FloatField(u'年初来安値')
    annual_min_price_deviation_ratio = models.FloatField(u'年初来安値乖離率')

    def __str__(self):
        return str(self.security_code) + ' ' + self.date.strftime('%Y/%m/%d')
