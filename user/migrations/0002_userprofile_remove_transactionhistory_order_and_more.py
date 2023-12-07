# Generated by Django 4.2.6 on 2023-12-03 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(default='profile/profile.jpg', upload_to='profle picture')),
                ('about', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='transactionhistory',
            name='order',
        ),
        migrations.RemoveField(
            model_name='transactionhistory',
            name='servicer',
        ),
        migrations.RemoveField(
            model_name='transactionhistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='EventsOrder',
        ),
        migrations.DeleteModel(
            name='TransactionHistory',
        ),
    ]
