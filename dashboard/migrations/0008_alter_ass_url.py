# Generated by Django 4.1.5 on 2023-03-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_ass_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ass',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
