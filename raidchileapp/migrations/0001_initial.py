# Generated by Django 2.1.7 on 2019-04-04 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='name')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='name')),
                ('icon', models.CharField(default='fa-eye', help_text='String from Font Awesome icons e.g. "fa-eye"', max_length=150, verbose_name='icon')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'feature',
                'verbose_name_plural': 'features',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='name')),
                ('region', models.CharField(blank=True, db_index=True, help_text='Helps users to search by coincidence.', max_length=150, verbose_name='region')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='name')),
                ('available', models.BooleanField(default=True, verbose_name='available')),
                ('tour_type', models.CharField(choices=[('HALF', 'Half-Day'), ('FULL', 'Full-Day')], max_length=4, verbose_name='type of tour')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('description', models.TextField(verbose_name='type of tour')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='duration (in hours)')),
                ('min_pax_number', models.PositiveSmallIntegerField(default=1, verbose_name='minimum passenger number')),
                ('adult_reg_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="adults' regular price")),
                ('children_reg_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="children's regular price")),
                ('adult_sale_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="adults' sale price")),
                ('children_sale_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="children's sale price")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tours', related_query_name='tour', to='raidchileapp.Category')),
                ('features', models.ManyToManyField(related_name='tours', related_query_name='tour', to='raidchileapp.Feature')),
                ('locations', models.ManyToManyField(related_name='tours', related_query_name='tour', to='raidchileapp.Location')),
            ],
            options={
                'verbose_name': 'tour',
                'verbose_name_plural': 'tours',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative', models.CharField(db_index=True, help_text='Description of the image.', max_length=150, verbose_name='alternative text')),
                ('image', models.ImageField(upload_to='tours_images/%Y/%m/%d', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('tours', models.ManyToManyField(related_name='images', related_query_name='image', to='raidchileapp.Tour')),
            ],
            options={
                'verbose_name': 'tour image',
                'verbose_name_plural': 'tour images',
                'ordering': ('alternative',),
            },
        ),
        migrations.AddIndex(
            model_name='tour',
            index=models.Index(fields=['id', 'slug'], name='raidchileap_id_f975ee_idx'),
        ),
    ]
