# Generated by Django 4.2.10 on 2024-02-17 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_news_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='id',
            field=models.CharField(default='7b5537a5-4e3e-41e7-a4ac-adfb5be57f23', editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]