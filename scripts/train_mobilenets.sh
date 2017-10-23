#!/bin/bash
#nohup 
python scripts/train_model.py \
--image_dir data/udacity_data_mix \
--summaries_dir model/summaries_udacity \
--validation_batch_size -1 \
--how_many_training_steps 4000 \
--architecture 'mobilenet_1.0_224' \
--keep_probabilities 0.5 \
--learning_rate 1e-2 \
--test_batch_size=-1 \
--print_misclassified_test_images
#> model/train.log 2>&1 &
