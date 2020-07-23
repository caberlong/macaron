from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

import tensorflow as tf

tf.keras.backend.set_floatx('float64')

mnist = tf.keras.datasets.mnist

# Load Data & Remove color channels
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channels dimension
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).shuffle(10000).batch(32)

test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

class MyModel(Model):
    def __init__(self,
                 loss_object,
                 optimizer,
                 train_loss,
                 train_metric,
                 test_loss,
                 test_metric):
        '''
            Setting all the variables for our model.
        '''
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 3, activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        self.d2 = Dense(10, activation='softmax')

        self.loss_object = loss_object
        self.optimizer = optimizer
        self.train_loss = train_loss
        self.train_metric = train_metric
        self.test_loss = test_loss
        self.test_metric = test_metric

    def nn_model(self, x):
        '''
            Defining the architecture of our model. This is where we run 
            through our whole dataset and return it, when training and 
            testing.
        '''
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)

    @tf.function
    def train_step(self, images, labels):
        '''
            This is a TensorFlow function, run once for each epoch for the
            whole input. We move forward first, then calculate gradients 
            with Gradient Tape to move backwards.
        '''
        with tf.GradientTape() as tape:
            predictions = self.nn_model(images)
            loss = self.loss_object(labels, predictions)
        gradients = tape.gradient(loss, self.trainable_variables)
        optimizer.apply_gradients(zip(
                                  gradients, self.trainable_variables))

        self.train_loss(loss)
        self.train_metric(labels, predictions)

    @tf.function
    def test_step(self, images, labels):
        '''
            This is a TensorFlow function, run once for each epoch for the
            whole input.
        '''
        predictions = self.nn_model(images)
        t_loss = self.loss_object(labels, predictions)

        self.test_loss(t_loss)
        self.test_metric(labels, predictions)

    def fit(self, train, test, epochs):
        '''
            This fit function runs training and testing.
        '''
        for epoch in range(epochs):
            for images, labels in train:
                self.train_step(images, labels)

            for test_images, test_labels in test:
                self.test_step(test_images, test_labels)

            template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
            print(template.format(epoch+1,
                                  self.train_loss.result(),
                                  self.train_metric.result()*100,
                                  self.test_loss.result(),
                                  self.test_metric.result()*100))

            # Reset the metrics for the next epoch
            self.train_loss.reset_states()
            self.train_metric.reset_states()
            self.test_loss.reset_states()
            self.test_metric.reset_states()

# Make a loss object
loss_object = tf.keras.losses.SparseCategoricalCrossentropy()

# Select the optimizer
optimizer = tf.keras.optimizers.Adam()

# Specify metrics for training
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_metric = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

# Specify metrics for testing
test_loss = tf.keras.metrics.Mean(name='test_loss')
test_metric = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

# Create an instance of the model
model = MyModel(loss_object = loss_object,
                optimizer = optimizer,
                train_loss = train_loss,
                train_metric = train_metric,
                test_loss = test_loss,
                test_metric = test_metric)

EPOCHS = 5

model.fit(train = train_ds,
          test = test_ds,
          epochs = EPOCHS)
