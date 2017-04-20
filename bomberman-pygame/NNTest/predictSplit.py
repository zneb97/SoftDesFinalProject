import numpy as np
import sys

import tensorflow as tf

def predict(input_mat):
    # Create the model
    num_feature = 25
    num_response = 6
    x = tf.placeholder(tf.float32, [None, num_feature])

    # Load input matrix
    mat = np.array(input_mat)

    # Start session
    sess = tf.InteractiveSession()

    # Load saved training model
    new_saver = tf.train.import_meta_graph('./walls.meta')
    new_saver.restore(sess,tf.train.latest_checkpoint('./'))

    # Load variables from trained model
    all_vars = tf.get_collection('vars')
    W = all_vars[0]
    b = all_vars[1]
    y = tf.matmul(x, W) + b

    # Find and return the action to take
    response_list = sess.run(y,feed_dict={x:[mat]})
    action = np.argmax(response_list[0])
    print(action)
    return action
if __name__ == "__main__":
    predict([1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,0,1,0,1])
