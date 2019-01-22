# Generated by Django 2.0.1 on 2018-01-04 15:30

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sitetree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('relative_url', models.CharField(db_index=True, editable=False, max_length=250, unique=True)),
                ('display_order', models.PositiveIntegerField(db_index=True, default=1, help_text='Controls order that pages are displayed')),
                ('content', models.TextField(blank=True)),
                ('head_title', models.CharField(blank=True, default='', help_text='Page Title for head. Max length 100 characters.', max_length=100)),
                ('meta_description', models.CharField(blank=True, default='', help_text='Page Meta Description Field. Max length 200 characters.', max_length=200)),
                ('header_image', filebrowser.fields.FileBrowseField(blank=True, help_text='Header image for the top of the page.', max_length=200)),
                ('is_hidden', models.BooleanField(default=False, help_text="Hidden pages do not show up in search or have a valid URL. They are useful for grouping similar pages by a parent page you don't want vislbe on the site")),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('nav_menu', models.ForeignKey(blank=True, help_text='An Optional navigation menu to display on this page.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sitetree.Tree')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='pages.Page')),
            ],
            options={
                'ordering': ('lft',),
            },
        ),
        migrations.CreateModel(
            name='PageTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Unique Name/ID for a template.', max_length=100, unique=True)),
                ('file_name', models.CharField(help_text='Full Path and file name of the template.', max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(blank=True, help_text='The template used to display this page. If blank the default template is used.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.PageTemplate'),
        ),
    ]