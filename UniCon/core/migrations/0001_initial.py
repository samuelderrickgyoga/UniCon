# Generated by Django 5.0.6 on 2024-05-27 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, null=True)),
                ('student_id', models.CharField(blank=True, max_length=20, null=True)),
                ('university', models.CharField(choices=[('makerere', 'Makerere'), ('kyambogo', 'Kyambogo'), ('kabaale', 'Kabaale'), ('gulu', 'Gulu'), ('muni', 'Muni'), ('soroti', 'Soroti'), ('lira', 'Lira'), ('busitema', 'Busitema'), ('mountains_of_the_moon', 'Mountains of the Moon')], max_length=30)),
                ('interests', models.CharField(blank=True, max_length=100)),
                ('year', models.CharField(choices=[('freshman', 'Freshman'), ('sophomore', 'Sophomore'), ('junior', 'Junior'), ('senior', 'Senior')], default='freshman', max_length=10)),
                ('firstname', models.CharField(blank=True, max_length=30)),
                ('lastname', models.CharField(blank=True, max_length=30)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('profile_picture', models.ImageField(default='avatar.jpg', upload_to='media')),
                ('course', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
