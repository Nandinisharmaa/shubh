# Generated by Django 3.2.6 on 2021-09-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_cart_orderplaced_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M', 'Mobile'), ('L', 'Laptop'), ('TW', 'Top Wear'), ('BW', 'Bottom Wear'), ('W', 'Women,s Wear'), ('K', 'Kid,s Wear'), ('E', 'Electronic')], max_length=20),
        ),
    ]
