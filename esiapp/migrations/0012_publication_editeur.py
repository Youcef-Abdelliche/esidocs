# Generated by Django 3.2.4 on 2021-06-30 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esiapp', '0011_alter_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='editeur',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]