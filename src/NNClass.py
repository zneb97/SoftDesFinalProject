"""
This module trains DNNs(Deep Neural Networks) on Tensorflow, using player's
own game play data as the training data. It also predicts the movements
of the player from observing the current status of the game using the DNN.

Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
By : TEAM AFK
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf  # Machine Learning Library


def my_input_fn(input):

    return np.array(input, dtype=np.float32)


class myClassifier:
    '''
    This class handles all the Neural Network operations for the bomberman
    including :
    1) training 2) prediction 3) weight visualization'''

    def __init__(self, trainName, saveStateName):
        '''
        Initalizes a Neural Network from the parameter config file
        "saveStatename". The dimensionality, hidden units, and output matrix must be changed
        according to the desired attributes of the Neural Network
        The parameter "trainName" is the file that the config will read from
        The header must have the number of data in the first column
        and the number of features in the second.
        '''

        self.saveStateName = saveStateName
        self.training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=trainName,
            target_dtype=np.int,
            features_dtype=np.int)
        feature_columns = [
            tf.contrib.layers.real_valued_column("", dimension=83)]
        self.classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                                         hidden_units=[
                                                             50, 25, 10],
                                                         n_classes=6,
                                                         model_dir=self.saveStateName)

    def get_test_inputs(self):
        '''helper function that feeds data to the classifier'''
        x = tf.constant(self.test_set.data)
        y = tf.constant(self.test_set.target)

        return x, y

    def get_train_inputs(self):
        '''helper function that feeds data to the classifier'''
        x = tf.constant(self.training_set.data)
        y = tf.constant(self.training_set.target)

        return x, y

    def trainModel(self, steps):
        '''
        Trains the model for a given number of iterations.
        The model must first be trained before predictions can be made,
        so it is possible to train it 0 times
        in order to load a modelwithout changes'''
        self.classifier.fit(input_fn=self.get_train_inputs, steps=steps)

    def testAccuracy(self, testName):
        '''
        Takes a csv file as input to test the accuracy of the model
        '''
        self.test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=testName,
            target_dtype=np.int,
            features_dtype=np.int)
        accuracy_score = self.classifier.evaluate(input_fn=self.get_test_inputs,
                                                  steps=1)["accuracy"]
        print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

    def predict(self, myInput):
        '''
        Return probability values that represent the prediction
        '''
        prediction = list(self.classifier.predict_proba(
            input_fn=lambda: my_input_fn(myInput)))
        return prediction[0]

    def returnvar(self):
        '''
        Returns the expected overall weight of each node
        on the neural network as a whole. This is hightly specialized for the
        current machine learning configuration and will therefore not work if
        any parameters change
        '''
        print(self.classifier.get_variable_names())
        finalWeights = self.classifier.get_variable_value('dnn/logits/weights')
        hl3Importance = []
        for i in range(10):
            ans = 0
            for j in range(6):
                ans += abs(finalWeights[i][j])
            hl3Importance.append(ans)
        twoWeights = self.classifier.get_variable_value(
            'dnn/hiddenlayer_2/weights')
        hl2Importance = []
        for i in range(25):
            ans = 0
            for j in range(10):
                ans += abs(twoWeights[i][j])
            hl2Importance.append(ans)
        oneWeights = self.classifier.get_variable_value(
            'dnn/hiddenlayer_1/weights')
        hl1Importance = []
        for i in range(50):
            ans = 0
            for j in range(25):
                ans += abs(oneWeights[i][j]) * hl2Importance[j]
            hl1Importance.append(ans)

        zeroWeights = self.classifier.get_variable_value(
            'dnn/hiddenlayer_0/weights')
        for i in range(83):
            if(i % 9 == 0 and i != 0):
                print(" ")
            ans = 0
            for j in range(30):
                ans += abs(zeroWeights[i][j]) * hl1Importance[j]
            print(int(ans), end=" ")


if __name__ == "__main__":

    ### COMMENT OUT THIS BLOCK IF YOU DON'T WANT TO TRAIN ###

    classx = myClassifier('training_data/wallsFULL.csv',
    "./WALLSCONFIGFULL")
    classx.trainModel(6000)

    classy = myClassifier('training_data/bombsFULL.csv',
    "./BOMBSCONFIGFULL")
    classy.trainModel(6000)

    classz = myClassifier('training_data/bricksFULL.csv',
    "./BRICKSCONFIGFULL")
    classz.trainModel(6000)

    classw = myClassifier('training_data/enemysFULL.csv',
    "./ENEMYSCONFIGFULL")
    classw.trainModel(6000)
