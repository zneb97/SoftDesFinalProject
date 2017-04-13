import numpy as np
import sys

import tensorflow as tf

def predict(bomb_mat, brick_mat, wall_mat):
    # Create the model
    num_feature = 25
    num_response = 6
    x1 = tf.placeholder(tf.float32, [None, num_feature])
    x2 = tf.placeholder(tf.float32, [None, num_feature])
    x3 = tf.placeholder(tf.float32, [None, num_feature])

    # Load input matrix
    bomb_mat = np.array(bomb_mat)
    brick_mat = np.array(brick_mat)
    wall_mat = np.array(wall_mat)

    # Start session
    sess = tf.InteractiveSession()

    # Load saved training model
    new_saver = tf.train.import_meta_graph('./surroundings.meta')
    new_saver.restore(sess,tf.train.latest_checkpoint('./'))

    # Load variables from trained model
    all_vars = tf.get_collection('vars')
    W1 = all_vars[0]
    W2 = all_vars[1]
    W3 = all_vars[2]
    b = all_vars[3]
    y = tf.matmul(x1, W1) + tf.matmul(x2, W2) + tf.matmul(x3, W3) + b

    # Find and return the action to take
    response_list = sess.run(y,feed_dict={x1: [bomb_mat], x2: [brick_mat], x3: [wall_mat]})
    action = np.argmax(response_list[0])
    return action
if __name__ == "__main__":
    print("Hello")
