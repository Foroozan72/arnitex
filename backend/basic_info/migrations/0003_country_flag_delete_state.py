# Generated by Django 4.2 on 2024-06-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0002_remove_city_tssssitle_state_title_alter_city_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='flag',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
