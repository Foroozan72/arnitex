# Generated by Django 4.2 on 2024-06-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_remove_ticketcontent_tracking_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('answered', 'Answered'), ('close', 'Close'), ('awaiting', 'Awaiting'), ('withdraw', 'Withdraw')], default='awaiting', max_length=10, verbose_name='Status'),
        ),
    ]
