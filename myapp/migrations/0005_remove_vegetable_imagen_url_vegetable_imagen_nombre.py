# Generated by Django 4.2.5 on 2023-10-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_vegetable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vegetable',
            name='imagen_url',
        ),
        migrations.AddField(
            model_name='vegetable',
            name='imagen_nombre',
            field=models.CharField(default='.png', max_length=100),
        ),
    ]
