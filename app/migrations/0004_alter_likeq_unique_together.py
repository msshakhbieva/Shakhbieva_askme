# Generated by Django 4.2.7 on 2023-11-15 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_likeq_unique_together_alter_question_text_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likeq',
            unique_together={('user', 'question')},
        ),
    ]