# Generated by Django 4.2.3 on 2023-09-02 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaint',
            old_name='user',
            new_name='customer',
        ),
    ]
