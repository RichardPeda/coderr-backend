# Generated by Django 5.1.1 on 2024-10-17 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_remove_offerdetail_delivery_time_in_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='offer_type',
            field=models.CharField(choices=[('bu', 'business'), ('cu', 'customer')], default='cu', max_length=10),
        ),
    ]
