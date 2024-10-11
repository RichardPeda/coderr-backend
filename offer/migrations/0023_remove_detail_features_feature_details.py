# Generated by Django 5.1.1 on 2024-10-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0022_rename_details_detail_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='features',
        ),
        migrations.AddField(
            model_name='feature',
            name='details',
            field=models.ManyToManyField(to='offer.detail'),
        ),
    ]
