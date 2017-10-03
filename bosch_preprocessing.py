import argparse
import yaml
from tqdm import tqdm
import os
import shutil

def process_yaml(yaml_file, data_path, output_path):
	DATA_DIR = data_path.strip('/') + '/'
	DST = output_path.strip('/')+'/'

	with open(DATA_DIR+yaml_file, 'r') as stream:
		try:
			print ("Reading {}".format(yaml_file))
			examples = yaml.load(stream)
			print ("{} is loaded into memeory. Processing".format(yaml_file))

			for image in tqdm(examples):
				PATH_TO_IMG = image['path']
				labels = set()
				tl_width = []
				occluded = set()
				for box in image['boxes']:
					labels.add(box['label'])
					x_width = (box['x_max']-box['x_min'])
					tl_width.append(x_width)
					occluded.add(box['occluded'])
				if len(labels) == 0:
					if not os.path.isdir(DATA_DIR+DST+'None'):
						os.makedirs(DATA_DIR+DST+'None')
					shutil.copy(DATA_DIR+PATH_TO_IMG[2:], DATA_DIR+DST+'None')
				elif len(labels) == 1:
					cls = list(labels)[0]
					if cls in {'Yellow', 'Green', 'Red'} and max(tl_width)>=15 and (False in occluded):
						if os.path.basename(PATH_TO_IMG) == '56988.png':
							cls = 'Red'
						if not os.path.isdir(DATA_DIR+DST+cls):
							os.makedirs(DATA_DIR+DST+cls)
						shutil.copy(DATA_DIR+PATH_TO_IMG[2:], DATA_DIR+DST+cls)
			print ("Done! \n")
		except Exception as exc:
		    print(exc)


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-y', '--yaml', dest='yaml_filename', required=True)
	parser.add_argument('-d', '--data_path', dest='data_path', required=True)
	parser.add_argument('-o', '--output_path', dest='output_path', required=True)

	args = parser.parse_args()

	process_yaml(args.yaml_filename, args.data_path, args.output_path)


if __name__ == '__main__':
	main()