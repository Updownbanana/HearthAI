#Import and configure libraries
from __future__ import print_function

import math

#from IPython import display
#from matplotlib import cm
#from matplotlib import gridspec
#from matplotlib import pyplot as plt


import numpy as np
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset
import xlrd


tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.1f}'.format

#Input function
def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
  #Convert pandas data into a dict of NumPy arrays
  features = {key:np.array(value) for key,value in dict(features).items}

  #Create a dataset from features and configure batching and repeating
  ds = Dataset.from_tensor_slices((features,targets))
  ds = ds.batch(batch_size).repeat(num_epochs)

  #Shuffle data if specified
  if shuffle:
    ds = ds.shuffle(buffer_size=10000)
  
  #Return the next batch of data
  features, labels = ds.make_one_shot_iterator().get_next()
  return features, labels

#Main modeling function
def train_model(learning_rate, steps, batch_size=1, periods=10):
  #Load dataset as "board_state_data"
  board_state_data = pd.read_excel('Hearthstone play data.xlsx','Processed Data')

  #Create a list of all features and feature column data
  features = []
  featureNames = ['Health','Opp. Health','Board','Opp. Board','Minions','Opp. Minions']
  for i in featureNames:
    features.append(board_state_data[[i]])

  #Attach the target to a variable
  targets = board_state_data[["Game Won"]]

  print ("RMSE for period:")
  #Create feature columns
  feature_columns = []
  for i in featureNames:
    feature_columns.append(tf.feature_column.numeric_column(i))

  #Create a gradient descent optimizer
  my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0000001)
  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  #Create a linear regression model with the feature columns and optimizer
  linear_regressor = tf.estimator.LinearRegressor(
    feature_columns=feature_columns,
    optimizer=my_optimizer
  )

  steps_per_period = steps / periods
  training_input_fn = lambda:my_input_fn(features, targets, batch_size=batch_size)
  prediction_input_fn = lambda:my_input_fn(features, targets, num_epochs=1, shuffle=False)

  #Train the model and compute loss each period
  for period in range(0,periods):
    #Train the model for 1 period
    linear_regressor.train(
      input_fn=training_input_fn,
      steps=steps_per_period
    )

    #Compute predictions and RMSE
    predictions = linear_regressor.predict(input_fn=prediction_input_fn)
    predictions = np.array([item['predictions'][0] for item in predictions])
    loss = math.sqrt(metrics.mean_squared_error(predictions, targets))
    #Print loss for period
    print ("  Period %02d : %0.2f" % (period, loss))

  print("Final training RMSE: %0.2f" % loss)
  return linear_regressor