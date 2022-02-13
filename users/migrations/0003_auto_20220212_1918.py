# Generated by Django 3.2.9 on 2022-02-13 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211226_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AddField(
            model_name='user',
            name='country_name',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AddField(
            model_name='user',
            name='ip_address',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='messaging_token',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='mining_rig_connected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='province',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='terms_agreed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default=None, max_length=13),
        ),
        migrations.AddField(
            model_name='user',
            name='verify_date',
            field=models.CharField(default=None, max_length=13),
        ),
        migrations.AddField(
            model_name='user',
            name='wallet_connected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=13),
        ),
    ]
