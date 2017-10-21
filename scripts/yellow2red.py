#!/home/ubuntu/anaconda3/bin/python
from glob import glob
import shutil
import os 
from tqdm import tqdm

path_udacity = '../data/udacity_data_mix/none/ud_224_yellow*.png'
path_sim = '../data/sim_binary/none/simyellow*.png'
ud_imgs = glob(path_udacity)
sim_imgs = glob(path_sim)
imgs = ud_imgs + sim_imgs 

def main():
	for img in tqdm(imgs):
		shutil(img, os.path.dirname(img)[:-4]+'red')
		
if __name__ == '__main__':
	main()

