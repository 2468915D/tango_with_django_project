# Generated by Django 3.1.5 on 2021-01-19 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20210115_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Catergories',
            },
        ),
        migrations.RemoveField(
            model_name='page',
            name='catergory',
        ),
        migrations.DeleteModel(
            name='Catergory',
        ),
        migrations.AddField(
            model_name='page',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='rango.category'),
            preserve_default=False,
        ),
    ]