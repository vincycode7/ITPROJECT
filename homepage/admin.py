from django.contrib import admin
from .models import User, usr_Image, face_model

# Register your models here.
admin.site.register(User)
admin.site.register(usr_Image)
admin.site.register(face_model)