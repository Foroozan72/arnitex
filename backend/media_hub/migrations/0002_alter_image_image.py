# Generated by Django 4.2 on 2024-07-09 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_hub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(help_text='Upload image with specific pixels', upload_to='media_hub/images/', verbose_name='Image'),
        ),
    ]
