#!/bin/bash
# connect to the instance with security key in ~/.ssh/
#
git clone https://github.com/olegleyz/traffic-light-classification.git
echo -e "\n downloading bosch dataset"
cd data
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.001
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.002
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.003
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.004
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.005
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.006
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_test_rgb.zip.007
cat dataset_test_rgb.zip* > dataset_test_rgb.zip
find . -type f -name 'dataset_test_rgb.zip.*' -delete
unzip dataset_test_rgb.zip
rm dataset_test_rgb.zip
rm non-commercial_license.docx
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_train_rgb.zip.001
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_train_rgb.zip.002
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_train_rgb.zip.003
wget https://s3-us-west-1.amazonaws.com/bosch-tl/dataset_train_rgb.zip.004
cat dataset_train_rgb.zip* > dataset_train_rgb.zip
find . -type f -name 'dataset_train_rgb.zip.*' -delete
unzip dataset_train_rgb.zip
rm dataset_train_rgb.zip
rm non-commercial_license.docx
cd ..
echo -e "\n installing dependencies"
pip install tensorflow-gpu
pip install tqdm
echo -e "\n preparing bosch dataset"
chmod +x "scripts/bosch_classif.py"
./scripts/bosch_classif.py

# downloading udacity dataset 
cd data
wget https://www.dropbox.com/s/fd4dr8k054dgo8w/udacity_data_mix.zip
unzip udacity_data_mix.zip