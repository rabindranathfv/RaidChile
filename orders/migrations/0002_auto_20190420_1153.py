# Generated by Django 2.1.7 on 2019-04-20 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', related_query_name='reservation', to='raidchileapp.Product', verbose_name='product'),
        ),
    ]