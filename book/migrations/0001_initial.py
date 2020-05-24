# Generated by Django 3.0.6 on 2020-05-21 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('read_status', models.CharField(choices=[('R', 'Read'), ('W', 'Want To Read'), ('C', 'Currently Reading')], max_length=2)),
                ('page_count', models.CharField(blank=True, max_length=6, null=True)),
                ('image_url', models.CharField(blank=True, max_length=50, null=True)),
                ('average_rating', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
