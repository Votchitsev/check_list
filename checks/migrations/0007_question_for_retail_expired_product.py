# Generated by Django 4.1 on 2024-04-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0006_question_sort_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='for_retail_expired_product',
            field=models.BooleanField(default=False, null=True, verbose_name='Для просроченных продуктов в буфете'),
        ),
    ]
