# Generated by Django 2.0.6 on 2018-06-20 18:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0002_auto_20180621_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='security',
            name='bps',
            field=models.FloatField(default=0, verbose_name='BPS'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='business',
            field=models.CharField(default='', max_length=1024, verbose_name='業種'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='dividend',
            field=models.IntegerField(default=0, verbose_name='1株配当'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='eps',
            field=models.FloatField(default=0, verbose_name='EPS'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='market',
            field=models.CharField(default=0, max_length=1024, verbose_name='市場'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='market_value',
            field=models.IntegerField(default=0, verbose_name='時価総額(百万円)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='pbr',
            field=models.FloatField(default=0, verbose_name='PBR'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='per',
            field=models.FloatField(default=0, verbose_name='PER'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='shares_number',
            field=models.IntegerField(default=0, verbose_name='発行済株式数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='security',
            name='unit_size',
            field=models.IntegerField(default=0, verbose_name='単元数'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='security',
            name='date',
            field=models.DateField(null=True, verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='security',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='銘柄名'),
        ),
    ]
