# Generated by Django 2.2 on 2020-05-08 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_auto_20200507_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='recommended',
            field=models.IntegerField(choices=[(4, '4.0'), (1, '1.0'), (3, '3.0'), (2, '2.0'), (5, '5.0')], default=2, verbose_name='推荐指数'),
        ),
    ]