from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None

def main():
  # Load datasets.
  training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
      filename="walls.csv",
      target_dtype=np.int,
      features_dtype=np.int)
  test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
      filename="wallsTest.csv",
      target_dtype=np.int,
      features_dtype=np.int)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 5])
  W = tf.Variable(tf.zeros([5, 5]))
  b = tf.Variable(tf.zeros([5]))
  y = tf.matmul(x, W) + b

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 5])

  # The raw formulation of cross-entropy,
  #
  #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
  #                                 reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
  # outputs of 'y', and then average across the batch.
  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()

  # Train
  # batch_xs, batch_ys = training_set.data, tf.one_hot(training_set.target,5)
  # sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys.eval()})

  #open the model
  new_saver = tf.train.import_meta_graph('./walls.meta')
  new_saver.restore(sess,tf.train.latest_checkpoint('./'))
  all_vars = tf.get_collection('vars')
  # for v in all_vars:
  #   v_ = sess.run(v)
  #   print(v_)
  W = all_vars[0]
  b = all_vars[1]
  y = tf.matmul(x, W) + b

  print('training complete')
  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: test_set.data,
                                      y_: tf.one_hot(test_set.target,5).eval()}))

if __name__ == '__main__':
  main()
