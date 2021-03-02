# Generated by Django 3.1.7 on 2021-03-01 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restapp', '0006_auto_20210301_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrolled_session',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrolled', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course_session',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='takes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='dob',
            field=models.DateField(blank=True, help_text='Enter you DOB'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, help_text='Enter you DOB'),
        ),
        migrations.AlterField(
            model_name='student',
            name='pin',
            field=models.IntegerField(blank=True),
        ),
    ]