# Generated by Django 3.2 on 2021-05-14 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_remove_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='placeholder', max_length=200, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=200),
        ),
    ]