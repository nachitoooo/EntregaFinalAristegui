# Generated by Django 4.2.4 on 2023-09-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]