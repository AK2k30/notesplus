# Generated by Django 4.1.5 on 2023-03-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_exx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exx',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='experi/covers/'),
        ),
        migrations.AlterField(
            model_name='exx',
            name='pdf',
            field=models.FileField(upload_to='experi/pdfs/'),
        ),
    ]
