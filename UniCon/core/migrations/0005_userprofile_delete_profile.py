# Generated by Django 5.0.6 on 2024-05-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_profile_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('university', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pics/')),
                ('course_of_study', models.CharField(max_length=100)),
                ('year_of_study', models.CharField(choices=[('freshman', 'Freshman'), ('sophomore', 'Sophomore')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]