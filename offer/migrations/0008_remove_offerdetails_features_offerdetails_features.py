# Generated by Django 5.1.1 on 2024-10-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0007_alter_offerdetails_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerdetails',
            name='features',
        ),
        migrations.AddField(
            model_name='offerdetails',
            name='features',
            field=models.ManyToManyField(to='offer.features'),
        ),
    ]