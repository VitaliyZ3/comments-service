# Generated by Django 4.2.2 on 2023-07-08 11:39

import core.service
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttachedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='File name')),
                ('image_src', models.FileField(blank=True, max_length=156, storage=core.service.UUIDFileStorage(), upload_to='', verbose_name='Image')),
                ('image_mini_src', models.FileField(blank=True, max_length=156, storage=core.service.UUIDFileStorage(is_miniature=True), upload_to='', verbose_name='')),
                ('file_src', models.FileField(blank=True, max_length=156, storage=core.service.UUIDFileStorage(is_document=True), upload_to='')),
            ],
            options={
                'verbose_name': 'Файли для чату',
            },
        ),
        migrations.CreateModel(
            name='UserCreator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='User name')),
                ('email', models.EmailField(max_length=30, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'UserCreator',
                'verbose_name_plural': 'UsersCreator',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Comment text')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='timestamp')),
                ('files', models.ManyToManyField(blank=True, related_name='comment', to='core.attachedfile', verbose_name='Attached files')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='core.comment', verbose_name='Parent comment')),
                ('user_creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment', to='core.usercreator')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]