# Generated by Django 3.1.7 on 2021-03-11 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0022_auto_20210311_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(help_text='Enter Course ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='restapp.course'),
        ),
    ]
