# Generated by Django 3.0.1 on 2019-12-23 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='numU',
            new_name='pacient_number',
        ),
    ]
