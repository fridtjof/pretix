# Generated by Django 3.0.9 on 2020-09-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banktransfer', '0008_remove_refundexport_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='refundexport',
            name='rows',
            field=models.TextField(default='[]'),
        ),
        migrations.DeleteModel(
            name='BankTransferRefund',
        ),
    ]
