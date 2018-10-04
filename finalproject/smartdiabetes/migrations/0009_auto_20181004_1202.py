# Generated by Django 2.1.2 on 2018-10-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartdiabetes', '0008_auto_20181004_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodglucoseresults',
            name='glucose',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, 'niezdefiniowana'), (1, 'mężczyzna'), (2, 'kobieta')], default=0, verbose_name='Płeć'),
        ),
    ]