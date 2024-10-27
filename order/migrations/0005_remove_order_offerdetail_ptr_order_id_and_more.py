# Generated by Django 5.1.1 on 2024-10-19 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0005_alter_detail_offer_type'),
        ('order', '0004_remove_order_detail_ptr_order_offerdetail_ptr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='offerdetail_ptr',
        ),
        migrations.AddField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='offer_detail',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_offer_detail', to='offer.offerdetail'),
            preserve_default=False,
        ),
    ]