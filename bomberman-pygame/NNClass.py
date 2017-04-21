from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import urllib

import numpy as np
import tensorflow as tf

def my_input_fn(input):

  return np.array(input, dtype=np.float32)

class myClassifier:
    def __init__(self,trainName, saveStateName):
        #  self.trainName = trainName
         self.saveStateName = saveStateName
        #  TRAINING = self.trainName
         self.training_set = tf.contrib.learn.datasets.base.load_csv_with_header(
             filename=trainName,
             target_dtype=np.int,
             features_dtype=np.int)
         feature_columns = [tf.contrib.layers.real_valued_column("", dimension=82)]
         self.classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                                     hidden_units=[10, 20, 10],
                                                     n_classes=6,
                                                     model_dir=self.saveStateName)
    def get_test_inputs(self):
        x = tf.constant(self.test_set.data)
        y = tf.constant(self.test_set.target)

        return x, y

    def get_train_inputs(self):
       x = tf.constant(self.training_set.data)
       y = tf.constant(self.training_set.target)

       return x, y
    def trainModel(self,steps):
        self.classifier.fit(input_fn=self.get_train_inputs, steps=steps)

    def testAccuracy(self, testName):
        self.test_set = tf.contrib.learn.datasets.base.load_csv_with_header(
              filename=testName,
              target_dtype=np.int,
              features_dtype=np.int)
        accuracy_score = self.classifier.evaluate(input_fn=self.get_test_inputs,
                                             steps=1)["accuracy"]
        print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

    def predict(self, myInput):
        prediction = list(self.classifier.predict_proba(input_fn=lambda: my_input_fn(myInput)))
        # print(
        #       "New Samples, Class Predictions:    {}\n"
        #       .format(prediction))
        # return np.random.choice(np.arange(0, 6), p=prediction[0])
        return prediction[0]

if __name__ == "__main__":
    classx = myClassifier('wallsFULL.csv', "./WALLSCONFIGFULL")
    classx.trainModel(2000)
    classy = myClassifier('bombsFULL.csv', "./BOMBSCONFIGFULL")
    classy.trainModel(2000)
    classz = myClassifier('bricksFULL.csv', "./BRICKSCONFIGFULL")
    classz.trainModel(2000)
    classw = myClassifier('enemysFULL.csv', "./ENEMYSCONFIGFULL")
    classw.trainModel(2000)

    classx.testAccuracy('wallsFULL.csv')
    # classx.predict([[1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,0,1]])
