# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import argparse
import sys
import numpy as np

import tensorflow as tf

def main():
    # Load datasets.
    training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename="walls.csv",
        target_dtype=np.int,
        features_dtype=np.int)

    # Create the model
    num_feature = 25
    num_response = 6
    x = tf.placeholder(tf.float32, [None, num_feature])
    W = tf.Variable(tf.zeros([num_feature, num_response]), name='W')
    b = tf.Variable(tf.zeros([num_response]),name='b')
    tf.add_to_collection('vars',W)
    tf.add_to_collection('vars',b)
    y = tf.matmul(x, W) + b

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, num_response])

    # Use tf.nn.softmax_cross_entropy_with_logits on the raw
    # outputs of 'y', and then average across the batch.
    # Use Gradient Descent to minize the loss
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    #Create saver and session
    saver = tf.train.Saver()
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # Train
    batch_xs, batch_ys = training_set.data, tf.one_hot(training_set.target,num_response)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys.eval()})
    saver.save(sess,'walls')
    print('training complete')

if __name__ == '__main__':
    main()
