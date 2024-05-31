from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to='_profile_images', null=True)

    class Meta:
        db_table = 'Profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user
    
class Task(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        order_with_respect_to = 'user'

    def __str__(self):
        return self.title