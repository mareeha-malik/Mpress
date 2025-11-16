# Generated migration for changing Post status choices from draft/published to pending/published

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('published', 'Published')],
                default='pending',
                max_length=20
            ),
        ),
    ]
