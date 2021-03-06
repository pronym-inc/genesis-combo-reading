# Generated by Django 3.2.8 on 2021-10-21 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_logentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='decrypted_content',
            field=models.TextField(db_index=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logentry',
            name='encryption_succeeded',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='content',
            field=models.TextField(),
        ),
    ]
