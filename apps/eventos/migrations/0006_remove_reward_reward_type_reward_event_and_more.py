# Generated by Django 4.1.7 on 2023-03-07 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventos', '0005_reward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='reward_type',
        ),
        migrations.AddField(
            model_name='reward',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward_event', to='eventos.evento'),
        ),
        migrations.AddField(
            model_name='reward',
            name='is_redeemed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reward',
            name='reward',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reward',
            name='bbcode',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reward', to='eventos.bbcode'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
