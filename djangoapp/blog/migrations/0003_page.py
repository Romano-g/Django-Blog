# Generated by Django 5.0.2 on 2024-02-24 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
                ('is_publisehd', models.BooleanField(default=False)),
                ('content', models.TextField()),
            ],
        ),
    ]
