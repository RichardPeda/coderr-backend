# Generated by Django 5.1.1 on 2024-10-07 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0013_alter_offer_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='details',
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('revisions', models.IntegerField()),
                ('delivery_time_in_days', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer_type', models.CharField(max_length=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.offer')),
            ],
        ),
        migrations.AddField(
            model_name='features',
            name='details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offer.details'),
        ),
        migrations.DeleteModel(
            name='OfferDetails',
        ),
    ]
