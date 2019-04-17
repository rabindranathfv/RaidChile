# Generated by Django 2.1.7 on 2019-04-16 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('raidchileapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(db_index=True, max_length=150, verbose_name='full name')),
                ('email', models.EmailField(max_length=100, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='phone')),
                ('message', models.TextField(blank=True, max_length=500, verbose_name='message')),
                ('trip_date', models.DateField(verbose_name="estimated first tour's date")),
                ('paid', models.BooleanField(default=False, verbose_name='paid?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_reg_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="adults' regular price")),
                ('children_reg_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="children's regular price")),
                ('adult_sale_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="adults' sale price")),
                ('children_sale_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="children's sale price")),
                ('adult_quantity', models.PositiveIntegerField(default=1, verbose_name='adults')),
                ('children_quantity', models.PositiveIntegerField(default=1, verbose_name='children')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', related_query_name='item', to='orders.Order', verbose_name='reservation order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', related_query_name='reservation', to='raidchileapp.Tour', verbose_name='tour')),
            ],
        ),
    ]
