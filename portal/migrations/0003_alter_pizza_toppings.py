# Generated by Django 5.1.4 on 2024-12-31 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_alter_pizza_toppings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='toppings',
            field=models.ManyToManyField(to='portal.topping'),
        ),
    ]