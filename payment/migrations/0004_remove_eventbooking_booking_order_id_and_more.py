# Generated by Django 4.2.6 on 2023-11-28 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_eventbooking_stripe_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventbooking',
            name='booking_order_id',
        ),
        migrations.RemoveField(
            model_name='eventbooking',
            name='booking_payment_id',
        ),
    ]
