# Generated by Django 5.1.1 on 2024-10-08 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0017_detail_features_delete_feature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='features',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
