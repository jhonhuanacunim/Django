# Generated by Django 4.2.5 on 2023-12-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_vegetable_preciocompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='direccion',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]