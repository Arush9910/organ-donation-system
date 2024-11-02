# Generated by Django 5.1.2 on 2024-11-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0013_remove_request_request_request_organ'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='organs',
            field=models.TextField(default='liver'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='parts',
        ),
    ]