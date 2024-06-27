# Generated by Django 5.0.6 on 2024-06-23 12:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avito', '0006_alter_post_create_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['status'], 'verbose_name': 'Отклики', 'verbose_name_plural': 'Отклики'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create_date'], 'verbose_name': 'Объявления', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['status'], name='avito_messa_status_4ca6c7_idx'),
        ),
    ]
