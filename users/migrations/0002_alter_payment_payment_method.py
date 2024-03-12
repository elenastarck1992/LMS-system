# Generated by Django 4.2.11 on 2024-03-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'наличные'), ('card', 'банковский перевод')], default='card', max_length=50, verbose_name='способ оплаты'),
        ),
    ]
