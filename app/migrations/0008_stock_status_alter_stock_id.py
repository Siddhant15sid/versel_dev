# Generated by Django 4.2.10 on 2024-02-18 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_stock_delete_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.CharField(default='542b88c1-e9ab-4bc2-885e-4b4e8d727819', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]