# Generated by Django 3.1.7 on 2021-03-06 20:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0018_auto_20210304_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter Evaluation Type', max_length=200, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Enter Topic', unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter moudule name', max_length=500, unique=True)),
                ('desc', models.TextField(help_text='Enter moudule description')),
                ('course', models.ForeignKey(help_text='Enter Course ', on_delete=django.db.models.deletion.CASCADE, to='restapp.course')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxmarks', models.IntegerField(help_text='Enter Maximum marks', validators=[django.core.validators.MaxValueValidator(100)])),
                ('questions', models.IntegerField(help_text='Enter  number of questions', validators=[django.core.validators.MaxValueValidator(50)])),
                ('start_time', models.DateTimeField(help_text='Enter  Start Date/Time')),
                ('end_time', models.DateTimeField(help_text='Enter end Date/Time')),
                ('course', models.ForeignKey(help_text='Enter Course Session ', on_delete=django.db.models.deletion.CASCADE, to='restapp.course_session')),
                ('evaluationtype', models.ForeignKey(help_text='Enter Evaluation Type', on_delete=django.db.models.deletion.CASCADE, to='restapp.evaluationtype')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
