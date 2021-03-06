# Generated by Django 2.1.2 on 2018-10-03 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartdiabetes', '0005_auto_20181003_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='carbo_grams',
            field=models.IntegerField(blank=True, default=0, verbose_name='Ile gram węglowodanów'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='fat_grams',
            field=models.IntegerField(blank=True, default=0, verbose_name='Ile gram tłuszczy'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Nazwa posiłku'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='protein_grams',
            field=models.IntegerField(blank=True, default=0, verbose_name='Ile gram białka'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='wbt',
            field=models.FloatField(blank=True, verbose_name='WBT'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ww',
            field=models.FloatField(blank=True, verbose_name='WW'),
        ),
        migrations.AlterField(
            model_name='temporarymenu',
            name='carbo_grams',
            field=models.IntegerField(blank=True, verbose_name='Ile gram węglowodanów'),
        ),
        migrations.AlterField(
            model_name='temporarymenu',
            name='fat_grams',
            field=models.IntegerField(blank=True, verbose_name='Ile gram tłuszczy'),
        ),
        migrations.AlterField(
            model_name='temporarymenu',
            name='protein_grams',
            field=models.IntegerField(blank=True, verbose_name='Ile gram białka'),
        ),
        migrations.AlterField(
            model_name='temporarymenu',
            name='wbt',
            field=models.FloatField(blank=True, verbose_name='WBT'),
        ),
        migrations.AlterField(
            model_name='temporarymenu',
            name='ww',
            field=models.FloatField(blank=True, verbose_name='WW'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(1, 'mężczyzna'), (2, 'kobieta'), (0, 'niezdefiniowana')], default=0, verbose_name='Płeć'),
        ),
    ]
