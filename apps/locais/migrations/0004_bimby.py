# Generated by Django 4.1.7 on 2023-03-02 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locais', '0003_local_latitude_local_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bimby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
    ]