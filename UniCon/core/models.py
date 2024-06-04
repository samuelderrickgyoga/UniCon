from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    student_id = models.CharField(max_length=20, null=True, blank=True)

    UNIVERSITY_CHOICES = [
        ('makerere', 'Makerere'), 
        ('kyambogo', 'Kyambogo'), 
        ('kabaale', 'Kabaale'), 
        ('gulu', 'Gulu'),
        ('muni', 'Muni'), 
        ('soroti', 'Soroti'), 
        ('lira', 'Lira'), 
        ('busitema', 'Busitema'), 
        ('mountains_of_the_moon', 'Mountains of the Moon')
    ]
    university = models.CharField(max_length=30, choices=UNIVERSITY_CHOICES)

    INTERESTS_CHOICES = [
        ('sports', 'Sports'), 
        ('music', 'Music'), 
        ('technology', 'Technology')
    ]
    interests = models.CharField(max_length=100, blank=True)

    COURSE_YEAR_CHOICES = [
        ('freshman', 'Freshman'), 
        ('sophomore', 'Sophomore'), 
        ('junior', 'Junior'), 
        ('senior', 'Senior')
    ]
    year = models.CharField(max_length=10, choices=COURSE_YEAR_CHOICES, default='freshman')

    firstname = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default="avatar.jpg")
    course = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True) 

    groups = models.ManyToManyField('Group', blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    communities = models.ManyToManyField('Community', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    no_of_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.caption

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name='group_members')

class Community(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name='community_members')
