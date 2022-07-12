# Generated by Django 4.0.5 on 2022-06-23 19:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_bookinstance_borrower_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['book', 'due_back'], 'permissions': [('can_mark_returned', 'Set book as returned')], 'verbose_name': 'Копия', 'verbose_name_plural': 'Копии книг'},
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ff6d3857-cefa-44b7-93e5-b08da1f20dd9'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'На обслуживании'), ('o', 'В аренде'), ('a', 'В наличии'), ('r', 'Зарезервирована')], default='m', max_length=10, verbose_name='Статус'),
        ),
    ]
