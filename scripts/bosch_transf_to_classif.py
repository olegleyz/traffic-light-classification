#!/home/ubuntu/anaconda3/bin/python
from tqdm import tqdm
import yaml
import os
import shutil
import cv2
import scipy.ndimage as spi
from random import randint
import numpy as np
import time

def shift(img, perc):
  rows,cols = img.shape[:2]
  shift_x = randint(0,int(cols * perc)) - int(cols * perc/2)
  shift_y = randint(0,int(rows * perc)) - int(rows * perc/2)
  return spi.shift(img, (shift_y,shift_x,0), mode='nearest')

def rotation(img, angle):
    angle = randint(0,angle) - int(angle/2)
    return spi.rotate(img, angle, axes=(1, 0), reshape=True, output=None, order=3, mode='nearest', cval=0.0, prefilter=True)

def flip(img, perc):
  prob = randint(0,100)
  if prob < 100 * perc:
    return np.fliplr(img)
  else:
    return img

def crop (img, perc):
  rows,cols = img.shape[:2]
  start_x = randint(0,int(perc*cols))
  end_x = cols - randint(0,int(perc*cols))
  width = end_x - start_x
  end_y = rows - randint(0,int(rows-width))
  start_y = end_y - width
  img = img [start_y:end_y, start_x:end_x, :]

  return cv2.resize(img, (cols,rows))

def color_jittering(img):
  r = randint(0,100)
  if r<20:
    noise_r = np.random.randint(0,15,(img.shape[0],img.shape[1]))
    noise_g = np.random.randint(0,15,(img.shape[0],img.shape[1]))
    noise_b = np.random.randint(0,15,(img.shape[0],img.shape[1]))
    zitter = np.zeros_like(img)
    zitter[:,:,0] = noise_r
    zitter[:,:,1] = noise_g
    zitter[:,:,2] = noise_b
    return cv2.add(img,zitter)
  else:
    return img

def shadow(img):
  top_y = img.shape[0] * np.random.uniform()
  top_x = 0
  bot_x = img.shape[1]
  bot_y = img.shape[0] * np.random.uniform()
  img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
  shadow_mask = 0*img_hls[:,:,1]
  X_m = np.mgrid[0:img.shape[0],0:img.shape[1]][0]
  Y_m = np.mgrid[0:img.shape[0],0:img.shape[1]][1]

  shadow_mask[((X_m-top_x)*(bot_y-top_y)-(bot_x-top_x)*(Y_m-top_y)>=0)]=1
  if np.random.randint(2)==1:
    random_bright=.8
    cond1 = shadow_mask==1
    cond0 = shadow_mask==0
    if np.random.randint(2)==1:
      img_hls[:,:,1][cond1]=img_hls[:,:,1][cond1]*random_bright
    else:
      img_hls[:,:,1][cond0]=img_hls[:,:,1][cond0]*random_bright
  return cv2.cvtColor(img_hls, cv2.COLOR_HLS2BGR)

def augment(img):
  img_c = crop(img, .5)
  img_c = rotation(img, 10)
  img_c = flip(img_c, .2)
  img_c = color_jittering(img_c)
  img_c = shadow(img_c)
  return img_c

def proc_yaml(yaml_file):
  labels_dic = {'Green':'green', 'Yellow':'yellow', 'Red':'red', 'off':'off'}
  img_type = 'jpg'
  date_stamp = time.strftime("%d%m%Y")
  with open(yaml_file, 'r') as stream:
    print("reading ", yaml_file)
    examples=yaml.load(stream)
    for j,elem in tqdm(enumerate(examples)):  
      occluded = []
      labels = []
      height = []
      xmin = []
      xmax = []
      write_flag = False

      for box in elem['boxes']:
        occluded.append(box['occluded'])
        labels.append(box['label'])
        height.append((box['y_max']-box['y_min'])/720)
        xmin.append(box['x_min'])
        xmax.append(box['x_max'])
      
      if len(set(labels)) == 1 and labels[0] in labels_dic.keys() and True in occluded and max(height)>=0.1:
        img_name = 'bosch_224_'+labels[0]+'_'+date_stamp+'_'+str(j)+'.'+img_type
        path = '../data/bosch_'+os.path.basename(yaml_file)[:-5]+'/'+labels_dic[labels[0]]
        write_flag = True
        
      elif len(labels) == 0:
        img_name = 'bosch_224_none_'+ date_stamp +'_'+str(j)+'.'+img_type
        path = '../data/bosch_'+os.path.basename(yaml_file)[:-5]+'/none'
        write_flag = True
        
      if (write_flag==True):
        if os.path.basename(yaml_file)[:-5] == 'test':
          img_file = '../data/rgb/test/'+os.path.basename(elem['path'])
        elif os.path.basename(yaml_file)[:-5] == 'train':
          img_file = '../data/' + elem['path'][2:]
        
        if os.path.isfile(img_file):
          if not os.path.exists(path):
            os.makedirs(path) 
          img = cv2.imread(img_file)
          x0 = int(max(min(min(xmin)-20,190),0))
          x1 = int(min(max(max(xmax)+20,1090),1280))
          
          img = img[:,x0:x1,:]
          img = cv2.resize(img, (224,224))
          #img = augment(img)
          cv2.imwrite(path+'/'+img_name, img)
        else:
          print ("Image ", img_file, " not found")

      if (j%100==0):
        print (j, " out of ", len(examples))

def main():
  dic_yaml = {0: '../data/train.yaml', 1: '../data/test.yaml', 2:'../data/additional_train.yaml'}
  for i in range(3):
    if os.path.isfile(dic_yaml[i]):
      proc_yaml(dic_yaml[i]) 
    else:
      print (dic_yaml[i], " not found")

if __name__ == '__main__':
  main()
