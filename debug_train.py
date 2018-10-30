"""This is the main class for debugging purpose"""
import tensorflow as tf

import source_dir.densenet_3d_estimator as estimator

MODEL_DIR = 'denseNet3d_result'
DATA_DIR = 'tfrecord'

HYPERPARAMETERS = {
    'num_classes': 6,
    'batch_size': 10,
    'initial_learning_rate': 0.1,
    'decay_step': 1000,
    'lr_decay_factor':
    0.1,  # Learning rate will decay by a factor for every decay_step
    'growth_rate': 12,  # Grows rate for every layer [12, 24, 40]
    'network_depth': 20,  # Depth of the whole network [20, 40, 250]
    'total_blocks': 3,  # Total blocks of layers stack
    'keep_prob': 0.9,  # Keep probability for dropout
    'weight_decay': 1e-4,  # Weight decay for L2 loss
    'model_type': 'DenseNet3D',
    'reduction': 0.5,  # Reduction rate at transition layer for the models
    'bc_mode': True,
    'num_frames_per_clip': 16,
    'crop_size': 128,
    'channel': 3,
    'train_total_video_clip': 21297,
    'eval_total_video_clip': 7008
}

TFRUNCONFIG = tf.estimator.RunConfig(
    log_step_count_steps=1, save_summary_steps=1, model_dir=MODEL_DIR)

CLASSIFIER = tf.estimator.Estimator(
    model_fn=estimator.model_fn, params=HYPERPARAMETERS, config=TFRUNCONFIG)

CLASSIFIER.train(
    input_fn=lambda: estimator.train_input_fn(DATA_DIR, HYPERPARAMETERS),
    steps=1)

CLASSIFIER.evaluate(
    input_fn=lambda: estimator.eval_input_fn(DATA_DIR, HYPERPARAMETERS),
    steps=1)

CLASSIFIER.export_savedmodel(
    export_dir_base=MODEL_DIR,
    serving_input_receiver_fn=
    lambda: estimator.serving_input_fn(HYPERPARAMETERS))