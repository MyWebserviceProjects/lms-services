# Generated by Django 3.1.7 on 2021-03-06 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0019_evaluation_evaluationtype_module_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='topics',
            field=models.ManyToManyField(help_text='Enter Topic ', to='restapp.Topic'),
        ),
    ]