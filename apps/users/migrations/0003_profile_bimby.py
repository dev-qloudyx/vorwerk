# Generated by Django 4.1.7 on 2023-03-02 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locais', '0004_bimby'),
        ('users', '0002_remove_profile_about_remove_profile_cidade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bimby',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='locais.bimby'),
            preserve_default=False,
        ),
    ]
