# Generated by Django 4.0.2 on 2022-02-23 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_problems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='profiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('desc', models.TextField(blank=True)),
                ('phone', models.CharField(max_length=11)),
                ('postal_address', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_api_model', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]