import os, sys
import shutil
import numpy as np
whole_dir = sys.argv[1]
from PIL import Image

def mkdir(path):
	try:
		os.mkdir(path)
	except:
		pass
train_path = os.path.join(whole_dir, 'train')
test_path = os.path.join(whole_dir, 'test')
mkdir(train_path)
mkdir(test_path)


organic_path_train = os.path.join(train_path, 'Organic')
mkdir(organic_path_train)
recycle_path_train = os.path.join(train_path, 'R')
mkdir(recycle_path_train)
poison_path_train = os.path.join(train_path, 'P')
mkdir(poison_path_train)
other_path_train = os.path.join(train_path, 'Other')
mkdir(other_path_train)

organic_path_test = os.path.join(test_path, 'Organic')
mkdir(organic_path_test)
recycle_path_test = os.path.join(test_path, 'R')
mkdir(recycle_path_test)
poison_path_test = os.path.join(test_path, 'P')
mkdir(poison_path_test)
other_path_test = os.path.join(test_path, 'Other')
mkdir(other_path_test)

count = 0
for file in os.listdir(whole_dir):
	if count == 0:
		print(file)
		count += 1
	if '.txt' in file:
		with open(os.path.join(whole_dir, file), 'r') as file_r:
			labels = file_r.read().splitlines()[0]
			img_path, sub_label = labels.split(', ')
			num_label = int(sub_label)  
			img = Image.open(os.path.join(whole_dir, img_path))
			flag = np.random.choice(np.asarray([1, 2]), p=[0.9, 0.1])
			flag = int(flag.astype('uint8'))
			if count == 1:
				print(flag)
				print(type(flag))
				count += 1

			if num_label <= 5:
				if flag == 1:
					img.save(os.path.join(other_path_train, img_path))
				else:
					img.save(os.path.join(other_path_test, img_path))

			elif num_label <= 13:
				if flag == 1:
					img.save(os.path.join(organic_path_train, img_path))
				else:
					img.save(os.path.join(organic_path_test, img_path))
			elif num_label <= 36:
				prob = np.random.choice(np.asarray([1, 2]), p=[0.2, 0.8])
				if int(prob.astype('uint8')) == 1:
					if flag == 1:
						img.save(os.path.join(recycle_path_train, img_path))
					else:
						img.save(os.path.join(recycle_path_test, img_path))
			else:
				if flag == 1:
					img.save(os.path.join(poison_path_train, img_path))
				else:
					img.save(os.path.join(poison_path_test, img_path))


