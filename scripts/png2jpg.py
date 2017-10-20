#!/home/ubuntu/anaconda3/bin/python
from glob import glob
import os
import cv2

def main():
	imgs = glob('data/dataset_mix/*/*.png')
	for img_file in tqdm(imgs):
		img = cv2.imread(img_file)
		img_name = os.path.basename(img_file)
		img_path = os.path.dirname(img_file)
		img_path_jpg = img_path[:16]+'_jpg'+img_path[16:]
		if not os.path.exists(img_path_jpg):
            os.makedirs(img_path_jpg) 
		img_file_jpg = os.path.join(img_path_jpg, img_name[:-3]+'jpg')
		cv2.imread(img_file_jpg, img)

if __name__ == '__main__':
	main()