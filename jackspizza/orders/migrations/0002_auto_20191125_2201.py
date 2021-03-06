# Generated by Django 2.2.7 on 2019-11-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_item', models.CharField(max_length=65)),
                ('small', models.DecimalField(decimal_places=2, max_digits=10)),
                ('large', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='pastaorder',
            name='user',
            field=models.CharField(default=None, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pizzaorder',
            name='user',
            field=models.CharField(default=None, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platterorder',
            name='user',
            field=models.CharField(default=None, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saladorder',
            name='user',
            field=models.CharField(default=None, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='suborder',
            name='user',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
    ]
