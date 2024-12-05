# Generated by Django 5.1.1 on 2024-12-04 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0008_alter_detail_price_alter_offer_min_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
