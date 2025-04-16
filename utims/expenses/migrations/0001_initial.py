# Generated by Django 5.1.6 on 2025-02-25 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('FOOD', 'Food'), ('SUPPLIES', 'Supplies'), ('UTILITIES', 'Utilities'), ('MISC', 'Miscellaneous')], max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='receipts/')),
            ],
        ),
    ]
