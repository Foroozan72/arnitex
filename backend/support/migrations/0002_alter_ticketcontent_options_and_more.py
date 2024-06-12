# Generated by Django 4.2 on 2024-06-08 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketcontent',
            options={'verbose_name': 'Ticket content', 'verbose_name_plural': 'Ticket contents'},
        ),
        migrations.AddField(
            model_name='ticketcontent',
            name='tracking_code',
            field=models.CharField(editable=False, max_length=13, null=True),
        ),
    ]