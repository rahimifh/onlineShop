# Generated by Django 5.0.9 on 2024-11-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_specialsale'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deliveryTime',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]