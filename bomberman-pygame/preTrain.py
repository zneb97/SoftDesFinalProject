# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import argparse
import sys
import numpy as np

import tensorflow as tf

def main():
    # Load datasets.
    bombs = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename="bombs.csv",
        target_dtype=np.int,
        features_dtype=np.int)
    bricks = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename="bricks.csv",
        target_dtype=np.int,
        features_dtype=np.int)
    walls = tf.contrib.learn.datasets.base.load_csv_with_header(
        filename="walls.csv",
        target_dtype=np.int,
        features_dtype=np.int)

    # Create the model
    num_feature = 25
    num_response = 6
    x1 = tf.placeholder(tf.float32, [None, num_feature])
    W1 = tf.Variable(tf.zeros([num_feature, num_response]), name='W1')
    x2 = tf.placeholder(tf.float32, [None, num_feature])
    W2 = tf.Variable(tf.zeros([num_feature, num_response]), name='W2')
    x3 = tf.placeholder(tf.float32, [None, num_feature])
    W3 = tf.Variable(tf.zeros([num_feature, num_response]), name='W3')
    b = tf.Variable(tf.zeros([num_response]),name='b')
    tf.add_to_collection('vars',W1)
    tf.add_to_collection('vars',W2)
    tf.add_to_collection('vars',W3)
    tf.add_to_collection('vars',b)
    y = tf.matmul(x1, W1) + tf.matmul(x2, W2) + tf.matmul(x3, W3) + b

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
    x1s, x2s, x3s, ys = bombs.data, bricks.data, walls.data, tf.one_hot(bombs.target,num_response)
    sess.run(train_step, feed_dict={x1: x1s, x2: x2s, x3: x3s, y_: ys.eval()})
    saver.save(sess,'surroundings')
    print('training complete')

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(sess.run(accuracy, feed_dict={x1: bombs.data, x2: bricks.data, x3: walls.data,
                                        y_: tf.one_hot(bombs.target,6).eval()}))

if __name__ == '__main__':
    main()
