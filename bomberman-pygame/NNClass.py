from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import urllib

import numpy as np
import tensorflow as tf


def my_input_fn(input):

    return np.array(input, dtype=np.float32)


class myClassifier:
    '''
    This class handles all the Neural Network operations for the bomberman including
    training, prediction and weight visualization'''

    def __init__(self, trainName, saveStateName):
        '''
        The init statement initalizes a NN from the parameter configuration file
        "saveStatename". If it does not exist, it will create a new NN will the given
        file name.

        The dimensionality, hidden units, and output matrix musst be changed in the code
        in accordance with the desired attributes of the Neural network

        The parameter "trainName" is the file that the config will read from
        The header of this file must have the number of data in  the first column
        and the number of features in the second.'''
       #  self.trainName = trainName
        self.saveStateName = saveStateName
       #  TRAINING = self.trainName
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
        '''helper function that will feed data to the classifier'''
        x = tf.constant(self.test_set.data)
        y = tf.constant(self.test_set.target)

        return x, y

    def get_train_inputs(self):
        '''helper function that will feed data to the classifier'''
        x = tf.constant(self.training_set.data)
        y = tf.constant(self.training_set.target)

        return x, y

    def trainModel(self, steps):
        '''This will train the model a given number of iterations.
        The model must first be trained before predictions can be made,
        so it is possible to train it 0 times in order to load a modelwithout changes'''
        self.classifier.fit(input_fn=self.get_train_inputs, steps=steps)

    def testAccuracy(self, testName):
        '''This function will take in a csv file to test the accuracy of the model'''
        self.test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
            filename=testName,
            target_dtype=np.int,
            features_dtype=np.int)
        accuracy_score = self.classifier.evaluate(input_fn=self.get_test_inputs,
                                                  steps=1)["accuracy"]
        print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

    def predict(self, myInput):
        '''This function will return probability values output by the model of a given input'''
        prediction = list(self.classifier.predict_proba(
            input_fn=lambda: my_input_fn(myInput)))
        # print(
        #       "New Samples, Class Predictions:    {}\n"
        #       .format(prediction))
        # return np.random.choice(np.arange(0, 6), p=prediction[0])
        return prediction[0]

    def returnvar(self):
        '''This function will return the expected overall weight of each node
        on the neural network as a whole. This is hightly specialized for the
        current machine learning configuration and will therefore not work if
        any parameters change'''
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
    # classx = myClassifier('wallsFULL.csv', "./WALLSCONFIGFULL")
    # classx.trainModel(6000)
    # classy = myClassifier('bombsFULL.csv', "./BOMBSCONFIGFULL")
    # classy.trainModel(6000)
    # classz = myClassifier('bricksFULL.csv', "./BRICKSCONFIGFULL")
    # classz.trainModel(6000)
    # classw = myClassifier('enemysFULL.csv', "./ENEMYSCONFIGFULL")
    # classw.trainModel(6000)
    # #
    classw = myClassifier('fakeEnemysFull.csv', "./ENEMYSCONFIGFULL")
    classw.returnvar()

    # classx.testAccuracy('wallsFULL.csv')
    # print(classx.returnvar())
    # classx.predict([[1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,0,1]])
