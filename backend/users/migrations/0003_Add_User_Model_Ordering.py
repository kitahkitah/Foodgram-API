# Generated by Django 4.0.7 on 2022-09-05 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_Adjust_User_Model_and_add_Token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',)},
        ),
    ]
