# Generated by Django 5.1.3 on 2025-02-06 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_comment_created_at_alter_like_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]
