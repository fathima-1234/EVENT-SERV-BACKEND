# Generated by Django 4.2.6 on 2023-11-27 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_number_of_members_eventbooking_numberofmembers'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbooking',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
