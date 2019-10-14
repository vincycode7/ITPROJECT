#importing manipulations of data
import numpy as np
\
#Model Act manipulation
import torch as tch
tch.nn.Module.dump_patches = True

from torchvision import datasets, models, transforms
from torch import nn, optim
import torch.nn.functional as F
from collections import OrderedDict
from PIL import  Image

class test_model:
  
  def __init__(self, url_for_cnn = 'cnnmodel_train.pt', url_for_fc='fcmodel_train.pt'):
    self.load_model(url_for_cnn, url_for_fc)

  def predict(self):

    #load models
    model = self.fc
    model.cpu().eval()
    cnn = self.cnn
    cnn.cpu().eval()

    #load data
    data = self.data
    img = data[:,:,:,:3]
    img2 = data[:,:,:,3:]
      
    img = cnn(tch.from_numpy(img.numpy().transpose((0, 3, 1, 2))))
    img2 = cnn(tch.from_numpy(img2.numpy().transpose((0, 3, 1, 2))))

    data = tch.cat((img,img2),1)

    # forward pass: compute predicted outputs by passing inputs to the model
    output = model(data)
    
    return output.cpu().detach().numpy(), output.cpu().topk(1)[1].detach().numpy()


  def load_model(self,url_for_cnn = 'cnnmodel_train.pt', url_for_fc='fcmodel_train.pt'):
    #testing model
    mod = tch.load(url_for_fc, map_location=tch.device('cpu'))
    fc = mod['model_arc']
    fc.load_state_dict(mod['state_dict'])
    self.fc = fc

    resnet = tch.load(url_for_cnn, map_location=tch.device('cpu'))
    cnn = resnet['model_arc']
    cnn.load_state_dict(resnet['state_dict'])
    self.cnn = cnn

    return cnn, fc

  def load_imgs(self, url_img_1=None, url_img_2=None):
    
    siz = 224
    chn = 6

    nw_dset = np.empty((0,siz,siz, chn))

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

    #concate images together as flatten
    con_img = np.expand_dims(np.c_[img,img2],0)
    img_d = np.copy(con_img)

    #convert imagw from numpy to tensor and add img to dataset
    nw_dset = np.r_[nw_dset,img_d]
    nw_dset = tch.tensor(nw_dset.astype(np.float32))
    self.data = nw_dset