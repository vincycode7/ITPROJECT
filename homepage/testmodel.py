#importing manipulations of data
import numpy as np

#Model Act manipulation
import torch as tch
tch.nn.Module.dump_patches = True

from torchvision import datasets, models, transforms
from torch import nn, optim
import torch.nn.functional as F
from collections import OrderedDict
from PIL import  Image

class test_model:
  
  def __init__(self, model=None):
    self.load_model(model)

  def predict(self):
    model = self.model
    model.cpu().eval()
    
    data = self.data.cpu()

    # forward pass: compute predicted outputs by passing inputs to the model
    output = model(data)
    
    return output.cpu().detach().numpy(), output.cpu().topk(1)[1].detach().numpy()


  def load_model(self,model=None):
    #testing model
    mod = tch.load(model, map_location=tch.device('cpu'))
    model = mod['model_arc']
    model.load_state_dict(mod['state_dict'])
    self.model = model

  def load_imgs(self, url_img_1=None, url_img_2=None):
    
    #transform image with pytorch
    trans = transforms.Compose([ transforms.Resize((224,224)),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406],
                                                              [0.229, 0.224, 0.225])])

    #load image1
    img = Image.open(url_img_1)
    img = trans(img).numpy().transpose((1, 2, 0))

    #load image2
    img2 = Image.open(url_img_2)
    img2 = trans(img2).numpy().transpose((1, 2, 0))

    #convert image from numpy to tensor and add img to dataset
    con_img = np.expand_dims(np.c_[img,img2],0)
    img_d = np.copy(con_img.transpose((0, 3, 1, 2)))  

    img_d = tch.tensor(img_d.squeeze(0).astype('float32'))
    self.data = img_d.unsqueeze(0)