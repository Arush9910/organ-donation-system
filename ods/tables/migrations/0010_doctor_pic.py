# Generated by Django 5.1.2 on 2024-10-31 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0009_hospital_pic_alter_hospital_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='pictures'),
        ),
    ]