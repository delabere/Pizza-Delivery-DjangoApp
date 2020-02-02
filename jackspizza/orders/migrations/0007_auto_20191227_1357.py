# Generated by Django 2.2.7 on 2019-12-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_pizzaorder_reg_pizza_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pastaorder',
            old_name='pasta_type',
            new_name='food_type',
        ),
        migrations.RenameField(
            model_name='pizzaorder',
            old_name='pizza_type',
            new_name='food_type',
        ),
        migrations.RenameField(
            model_name='platterorder',
            old_name='platter_type',
            new_name='food_type',
        ),
        migrations.RenameField(
            model_name='saladorder',
            old_name='salad_type',
            new_name='food_type',
        ),
        migrations.RenameField(
            model_name='suborder',
            old_name='sub_type',
            new_name='food_type',
        ),
        migrations.AlterField(
            model_name='pastaorder',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Complete', 'Complete')], max_length=20),
        ),
        migrations.AlterField(
            model_name='pizzaorder',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Complete', 'Complete')], max_length=20),
        ),
        migrations.AlterField(
            model_name='platterorder',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Complete', 'Complete')], max_length=20),
        ),
        migrations.AlterField(
            model_name='saladorder',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Complete', 'Complete')], max_length=20),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Complete', 'Complete')], max_length=20),
        ),
    ]