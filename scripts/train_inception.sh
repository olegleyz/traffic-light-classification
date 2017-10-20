#!/bin/bash
nohup python src/retrain.py \
--image_dir data/dataset_mix_jpg \
--summaries_dir model/summaries_inception \
--random_brightness 5 \
--validation_batch_size -1 \
--how_many_training_steps 4000 \
--test_batch_size -1 \
--print_misclassified_test_images > model/train_inc.log 2>&1 &
