git clone https://github.com/olegleyz/traffic-light-classification.git
cd traffic-light-classification
git clone https://github.com/tensorflow/tensorflow.git

# train
python src/retrain.py \
--image_dir data/sim_data \
--output_graph model/train \
--intermediate_output_graphs_dir model/train/intermediate \
--output_labels model/train \
--summaries_dir model/summaries \
--how_many_training_steps 20 \
--validation_batch_size -1 \
--print_misclassified_test_images model/train/misclassif\
--bottleneck_dir model/bottleneck \
--flip_left_right 5 \
--random_crop 5 \
--random_scale 5 \
--random_brightness 5 \
--architecture 'mobilenet_1.0_224'
#--final_tensor_name 'output-tensor' \
#--learning_rate 0.004 \
#--testing_percentage 0 \
#--validation_percentage 20 \

# train 2
python src/retrain.py \
--image_dir data/sim_data \
--summaries_dir model/summaries \
--flip_left_right 5 \
--random_crop 5 \
--random_scale 5 \
--random_brightness 5 \
--architecture 'mobilenet_1.0_224'

# train 3 PID 1684
nohup python src/retrain.py \
--image_dir data/udacity_data \
--summaries_dir model/summaries_udacity \
--flip_left_right 5 \
--random_crop 5 \
--random_scale 5 \
--random_brightness 5 \
--architecture 'mobilenet_1.0_224'> model/train.log 2>&1 &

# tensorboard
nohup tensorboard --logdir model/summaries_sim > model/tensorboard.log 2>&1 &


nohup python src/retrain_sim.py \
--image_dir data/ \
--summaries_dir model/summaries_sim \
--flip_left_right 5 \
--random_brightness 5 \
--validation_batch_size -1 \
--how_many_training_steps 1000 \
--print_misclassified_test_images model/misclassif > model/train.log 2>&1 &

nohup python src/retrain_sim.py \
--image_dir data/ \
--summaries_dir model/summaries_sim \
--flip_left_right 5 \
--random_brightness 5 \
--validation_batch_size -1 \
--how_many_training_steps 11 \
--print_misclassified_test_images model/misclassif > model/train.log 2>&1 &

 \
--architecture 'mobilenet_1.0_224'> model/train.log 2>&1 &

# git clone https://github.com/olegleyz/traffic-light-classification.git



# instance for data 17102017 and inception
# ec2-54-193-16-201.us-west-1.compute.amazonaws.com
# wget https://www.dropbox.com/s/s0rhn57y048jea8/sim17102017.zip
# wget https://www.dropbox.com/s/sbjtckjnjcyv20e/sim_test.zip
# PID retrain 25319
# PID tensorboard 25370

# instance for data 17102017 and mobilenet
# ec2-13-56-253-162.us-west-1.compute.amazonaws.com
