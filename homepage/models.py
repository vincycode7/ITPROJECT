from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    firstname = models.CharField (max_length=20)
    middlename = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to="images/", null=True,)

    def __str__(self):
        return  self.username

class usr_Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image1 = models.CharField(max_length=20,null=True)
    image2 = models.ImageField(upload_to="users/", unique=True, null=True)
    prediction = models.IntegerField(null=True)
    accuracy = models.FloatField(null=True)
    correct_prediction = models.IntegerField(null=True)

    def __str__(self):
        return self.image2.url.split("/")[-1]

class face_model(models.Model):
    model = models.FileField(upload_to="face_model/", null=True)

    def __str__(self):
        return self.model.url.split("/")[-1]