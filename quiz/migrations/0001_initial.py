# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=256)),
                ('definition', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Has',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.ForeignKey(to='quiz.Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('name', models.CharField(max_length=256, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256, null=True)),
                ('language_from', models.ForeignKey(related_name='language_from', to='quiz.Language')),
                ('language_to', models.ForeignKey(related_name='language_to', to='quiz.Language')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='set',
            name='user',
            field=models.ForeignKey(to='quiz.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='set',
            unique_together=set([('user', 'title')]),
        ),
        migrations.AddField(
            model_name='has',
            name='set',
            field=models.ForeignKey(to='quiz.Set'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='has',
            unique_together=set([('class_name', 'set')]),
        ),
        migrations.AddField(
            model_name='class',
            name='user',
            field=models.ForeignKey(to='quiz.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together=set([('name', 'user')]),
        ),
        migrations.AddField(
            model_name='card',
            name='set',
            field=models.ForeignKey(to='quiz.Set'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('set', 'term', 'definition')]),
        ),
    ]
