# Generated by Django 3.2.3 on 2021-05-28 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proyecto', '0010_apartadosaplicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartadosaplicacion',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Proyecto.proyecto'),
        ),
    ]
