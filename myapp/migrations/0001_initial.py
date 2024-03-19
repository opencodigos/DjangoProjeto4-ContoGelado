# Generated by Django 4.1.4 on 2024-03-18 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Embalagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('capacidade_maxima_bolas', models.PositiveIntegerField()),
                ('ativo', models.BooleanField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': '1 - Embalagem',
                'verbose_name_plural': '1 - Embalagem',
            },
        ),
    ]