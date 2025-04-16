# Generated by Django 5.1.6 on 2025-02-25 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('FOOD', 'Food'), ('SUPPLIES', 'Supplies'), ('GROCERIES', 'Groceries'), ('UTILITIES', 'Utilities'), ('MISC', 'Miscellaneous')], max_length=20),
        ),
    ]
