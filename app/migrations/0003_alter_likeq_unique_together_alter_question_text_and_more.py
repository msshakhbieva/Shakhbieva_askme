# Generated by Django 4.2.7 on 2023-11-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_question_text'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likeq',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]