# Generated by Django 3.2.6 on 2021-09-02 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_remove_user_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.CharField(max_length=64, null=True, verbose_name='아이디'),
        ),
    ]
