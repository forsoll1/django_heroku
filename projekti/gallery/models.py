from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import FileExtensionValidator
from django.forms import Form
from random import randint

def user_directory_path(instance, filename):
    randomizer = "_"+str(randint(1,999))
    file, ext = os.path.splitext(filename)
    filefolder = file+randomizer
    new_name = file+randomizer+ext
    return 'user_{0}/{1}/{2}'.format(instance.user.username, filefolder, new_name)

class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    img_file = models.ImageField(upload_to = user_directory_path)
    img_thumb = models.ImageField(upload_to = 'media/', blank=True)
    img_s = models.ImageField(upload_to = 'media/', blank=True)
    img_m = models.ImageField(upload_to = 'media/', blank=True)
    img_l = models.ImageField(upload_to = 'media/', blank=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)

