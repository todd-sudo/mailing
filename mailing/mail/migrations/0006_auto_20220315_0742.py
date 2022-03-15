# Generated by Django 3.2.12 on 2022-03-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0005_alter_message_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='client',
        ),
        migrations.AddField(
            model_name='message',
            name='clients',
            field=models.ManyToManyField(related_name='messages', to='mail.Client', verbose_name='Клиенты'),
        ),
    ]