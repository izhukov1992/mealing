# Generated by Django 2.0.2 on 2018-03-03 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='initiated',
            field=models.CharField(choices=[('Client', 'Client'), ('Trainer', 'Trainer')], default='Client', max_length=255),
        ),
    ]