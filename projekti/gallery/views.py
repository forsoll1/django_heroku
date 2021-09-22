from django.shortcuts import render, redirect
from .models import Image
from django.conf import settings
from .forms import ImageForm

from PIL import Image as pil
import os
import re
from django.utils import timezone
from django.core.exceptions import PermissionDenied

def home(request):
    images = []
    if request.user.is_authenticated:
        images = Image.objects.filter(user = request.user)
    return render(request, 'home.html', {'images': images})

def show_image(request, image_id):
    current_user = request.user
    chosen_image = Image.objects.filter(id = image_id)[0]
    context = { 'image':chosen_image,
                'auth':current_user.is_authenticated }
    return render(request, 'showimage.html', context)

def delete(request, image_id):
    if request.user.is_authenticated and request.user == Image.objects.get(id=image_id).user:
        chosen_image = Image.objects.filter(id = image_id)[0]
        if delete_files_and_folder(chosen_image, request.user):
            chosen_image.delete()
        else: 
            print("Could not delete files, database entry won't be deleted")
        return redirect('home') 
    else:
        raise PermissionDenied()

def delete_files_and_folder(chosen_image, user):
        file, ext = os.path.splitext(chosen_image.img_file.name)
        filename = re.split(r'\/', file)[-1]
        del_folder = f"{settings.BASE_DIR}{settings.MEDIA_URL}user_{user.username}/{filename}"

        try: 
            for f in os.listdir(del_folder):
                os.remove(f"{del_folder}/{f}")   
            os.rmdir(del_folder)
        except(Exception):
            print("Could not delete folder/files.")
            return False
        return True

def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            current_time = timezone.now()
            current_user = request.user            

            image_instance = Image()
            image_instance.user = current_user
            image_instance.pub_date = current_time
            image_instance.img_file = request.FILES['img_file']
            image_instance.description = request.POST['description']
            image_instance.save()

            saved = Image.objects.filter(pub_date = current_time)[0]

            img_path = saved.img_file.path
            im = pil.open(img_path)

            if im.width>1024:
                resized = resize(3, im, img_path)
            elif im.width > 640 and im.width <= 1024:
                resized = resize(2, im, img_path)
            else: 
                resized = resize(1, im, img_path)
            thumb = create_thumbnail(im, img_path)

            saved.img_l = resized['large']
            saved.img_m = resized['medium']
            saved.img_s = resized['small']
            saved.img_thumb = thumb
            saved.save()

            return redirect('home') 
    else:
        form = ImageForm()
    
    return render(request, 'upload.html', {'form':form})

def resize(key, im, img_path):
    file, ext = os.path.splitext(img_path)
    names = ['small', 'medium', 'large']
    resolutions = [320, 640, 1024]
    result = {}
    width, height = im.size
    ratio = width/height

    for i in range(0,key):
        path = file + f"_{names[i]}{ext}"
        new_width = resolutions[i]
        new_height = new_width/ratio
        new_image = im.resize((round(new_width), round(new_height)), pil.ANTIALIAS)
        new_image.save(path, )
        result[names[i]] = re.split("/media/", path, 1)[-1]
    
    if 'medium' not in result: result['medium'] = result['small']
    if 'large' not in result: result['large'] = result['medium']

    return result

def create_thumbnail(im, img_path):
    used_image = pil.open(img_path)
    file, ext = os.path.splitext(img_path)
    path = file+"_thumb"+f"{ext}"
    new_path = re.split("/media/", path, 1)[-1]
    
    size = (180,180)
    im.thumbnail(size)
    im.save(path)
    return new_path
   