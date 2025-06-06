# Generated by Django 5.2.1 on 2025-05-21 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_cartitem_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='session_key',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='notes.order'),
        ),
    ]
