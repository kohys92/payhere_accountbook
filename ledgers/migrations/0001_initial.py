# Generated by Django 3.2.9 on 2021-11-19 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('note', models.CharField(max_length=200)),
                ('income', models.IntegerField(blank=True, default=0, null=True)),
                ('expense', models.IntegerField(blank=True, default=0, null=True)),
                ('total', models.IntegerField()),
                ('category', models.CharField(max_length=45)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'ledgers',
            },
        ),
    ]