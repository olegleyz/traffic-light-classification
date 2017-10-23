#!/bin/bash
nohup python src/retrain.py \
--image_dir data/dataset_mix_jpg \
--summaries_dir model/summaries_sim \
--random_brightness 5 \
--validation_batch_size -1 \
--how_many_training_steps 4000 \
--architecture 'mobilenet_1.0_224' \
--keep_probabilities 0.5 \
--learning_rate 1e-3 \
--test_batch_size=-1 \
--print_misclassified_test_images > model/train.log 2>&1 &
