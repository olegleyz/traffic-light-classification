# Traffic Light Image Classification  
Udacity Self-Driving Car Nanodegree  
Capstone Project. System Integration  

#### Overview  
As part of the perception subsystem the car should classify the color of traffic lights on it's way.  
In the given simulator and test site environment car faces single traffic light or a set of 3 traffic lights in the same state (green, yellow, red). We assume it's not possible to have multiple traffic lights in the different states at the same time.

We've considered different approaches to solve the traffic ligth classification task:
*  classification of the entire image using CNN; 
*  object (traffic light in state) detection;  
*  object (traffic light) detection and classification using separate model.  

Considering the fact, that traffic lights are always in the same state, and focusing on the creating of the ligth and fast model, we've chosen the way of the entire image classfication.  
This approach assumes usage of the Convolutional Neural Network, which takes the entire image from the frontal camera as an input and outputs the traffic ligth state (we've decided to use Red / Non-red prediction classes) as an output. We've used transfer learning with Mobilenet model, available as Tensorflow image retrain example. 

## Dataset  
There are multiple datasets, available for model training:  
*  images from the Udacity Simulator (images as well as the ground truth from the frontal camera are available as a ROS topic);  
https://drive.google.com/open?id=0Bw5abyXVejvMci03bFRueWVXX1U
*  rosbag, captured on the Udacity's test site;  
https://drive.google.com/file/d/0B2_h37bMVw3iYkdJTlRSUlJIamM/view  
*  Bosch Small Traffic Lights Dataset.  
We've trained our model on a mixture of the datasets above.  

## Image pre-processing
On the image pre-processing step we've applied multiple visual transformations:  
random cropping of the image;  
rotation on the random angle (+/- 5 degrees);  
random flipping of the up to 20% images;  
random color jittering;  
applying shadows (reference: https://goo.gl/VzoxcY).  
In order to slightly balance dataset, some images (manually chosen) were augmented.  
  
## Neural Network Model
"Simple transfer learning with Mobilenet model" example from Tensorflow was used to re-train our model.  
We took a Mobilenet model, pre-trained on the ImageNet images, and trained a new set of fully connected layers with dropout, which can recognize our traffic light classes of images.   
Model works with the image's dimension 224x224x3, the top layer receives as input a 1001-dimensional for for each image. 


Accuracy on the simulator data: 
![](model/sim_accuracy.png)
  
Accuracy on the Udacity's test track data: 
![](model/udacity_accuracy.png)

## Usage
### Train 

```
nohup python src/retrain.py \
--image_dir data/udacity_data \
--summaries_dir model/summaries_udacity \
--flip_left_right 5 \
--random_crop 5 \
--random_scale 5 \
--random_brightness 5 \
--architecture 'mobilenet_1.0_224'> model/train.log 2>&1 &
```

### Tensorboard

```
nohup tensorboard --logdir model/summaries_udacity > model/tensorboard.log 2>&1 &
```
