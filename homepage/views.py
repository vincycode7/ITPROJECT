from django.shortcuts import render
from .models import User, usr_Image, face_model
import base64
from django.core.files.base import ContentFile
from datetime import date, datetime
import time, json
from .testmodel import test_model

#importing manipulations of data
import numpy as np

# #Model Act manipulation
import torch as tch
#tch.nn.Module.dump_patches = False

from torchvision import datasets, models, transforms
from torch import nn, optim
import torch.nn.functional as F
from collections import OrderedDict
from PIL import  Image

# Create your views here.


#get cnn and fc pathsgit
mods = face_model.objects.filter(id=1)
cnn = mods[0].cnn_model
fc = mods[0].fc_model

#instatiat the face detector
face_dec = test_model(cnn, fc)

#index page
def index(request):
    return render(request, 'homepage/index.html')

# login with username and password
def login(request):

    #if user submits a form, then check if user is available
    if request.POST:
        users = User.objects.filter(username = request.POST["username"])

        # if user is found in database proceed to authentication
        if len(users) != 0 and users[0].password == request.POST["password"]:
            return render(request, 'homepage/signin.html', {'data':
                                                                    json.dumps(
                                                                        {
                                                                            'login' : 1, 
                                                                            'username' : users[0].username,
                                                                            'prediction' : ""
                                                                        }
                                                                    )
            })

        #if user not found, then abort
        else:
            return render(request, 'homepage/signin.html', {'data':
                                                                    json.dumps(
                                                                        {
                                                                            'login' : 0, 
                                                                            'username' : "",
                                                                            'prediction' : ""
                                                                        }
                                                                    )
            })
    #if a form wasnt submitted, then abort
    else:
        return render(request, 'homepage/signin.html', {'data':
                                                                    json.dumps(
                                                                        {
                                                                            "login" : "", 
                                                                            "username" : "",
                                                                            "prediction" : ""
                                                                        }
                                                                    )
                                                        }
)


#authenticate the user
def authusr(request):
    
    #if user submits a form, then check if user is available
    try:
        #get user
        user = User.objects.filter(username = request.POST["username"])
        
        #get image from the form
        data = request.POST["img2"]

        #split and decode image
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr)) 

        #get current date and time to save image as Month abbreviation, day and year 
        today = date.today()	
        now = datetime.now()

        current_date = today.strftime("%b-%d-%Y")
        current_time = now.strftime("%H-%M-%S")

        #save image
        filename = request.POST["username"] + "_" +str(current_date) + "_" + current_time + "." + ext
        inst = usr_Image()
        inst.user = user[0]
        inst.image1 = user[0].profile_picture
        inst.image2.save(filename, data, save=True)


        #load first and second image from database
        image1 = inst.image1
        image2 = inst.image2

        #load images
        face_dec.load_imgs(image1, image2)

        #predict
        accuracy, prediction = face_dec.predict()

        prediction = prediction[0][0]

        accuracy = accuracy[0][0] if prediction == 0 else accuracy[0][1]
        
        #saving prediction and accuracy
        inst.prediction = prediction
        inst.api_accuracy = accuracy
        inst.save()
        
        if prediction == 0:
            return render(request, 'homepage/signin.html',{'data':
                                                                    json.dumps(
                                                                        {
                                                                            'login' : 1, 
                                                                            'username' : request.POST["username"],
                                                                            'prediction' : 0
                                                                        })
            })
            
        else:
            return render(request, 'testapp/index.html', {'data':
                                                                    json.dumps(
                                                                        {
                                                                            'login' : 1, 
                                                                            'username' : request.POST["username"],
                                                                            'prediction' : 1
                                                                        })
    
            })

    except:
            return render(request, 'homepage/signin.html', {'data':
                                                                        json.dumps(
                                                                        {
                                                                            'login' : "", 
                                                                            'username' : "",
                                                                            'prediction' : ""
                                                                        })
                })