# Generated by Django 2.0.2 on 2018-03-01 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180301_1520'),
        ('meal', '0002_auto_20180215_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='user',
        ),
        migrations.AddField(
            model_name='meal',
            name='client',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.Client'),
            preserve_default=False,
        ),
    ]
