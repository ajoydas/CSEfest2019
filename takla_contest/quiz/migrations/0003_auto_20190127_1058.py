# Generated by Django 2.1.2 on 2019-01-27 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190118_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='answer',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]