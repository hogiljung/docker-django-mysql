# Generated by Django 4.1.2 on 2023-01-19 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_contents_table_alter_post_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='post', serialize=False, to='board.post', unique=True)),
                ('content', models.TextField(max_length=100)),
                ('large_content', models.TextField()),
            ],
            options={
                'db_table': 'post_content',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Contents',
        ),
    ]
