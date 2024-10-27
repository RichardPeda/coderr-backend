# Generated by Django 5.1.1 on 2024-10-17 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0005_alter_detail_offer_type'),
        ('order', '0003_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='detail_ptr',
        ),
        migrations.AddField(
            model_name='order',
            name='offerdetail_ptr',
            field=models.OneToOneField(auto_created=True, default=2, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='offer.offerdetail'),
            preserve_default=False,
        ),
    ]