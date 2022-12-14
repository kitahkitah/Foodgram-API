# Generated by Django 4.0.7 on 2022-09-06 10:39

from django.db import migrations, models
import recipes.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', recipes.fields.HEXColor(blank=True, max_length=7, verbose_name='цвет в HEX')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Уникальный slug')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
