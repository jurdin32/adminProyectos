# Generated by Django 3.2.3 on 2021-05-28 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyecto', '0007_auto_20210528_0956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diagramaprocesos',
            options={'verbose_name_plural': 'E5 Diagrama de procesos'},
        ),
        migrations.AddField(
            model_name='diagramaprocesos',
            name='tipo',
            field=models.CharField(default='PROCESOS', max_length=30),
        ),
    ]