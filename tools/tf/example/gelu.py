import tensorflow as tf
import math

def gelu(x):
    return 0.5*x*(1+tf.tanh(tf.sqrt(2/math.pi)*(x+0.044715*tf.pow(x, 3))))

def get_gradient(x, activation_function):
    with tf.GradientTape() as gt:
        y = activation_function(x)
        gradient = gt.gradient(y, x).numpy()
        return gradient

x = tf.Variable(0.5)
gradient = get_gradient(x, gelu)

print('{0} is the gradient of GELU with x={1}'.format(
    gradient, x.numpy()
))

import timeit
conv_layer = tf.keras.layers.Conv2D(100, 3)

@tf.function
def conv_fn(image):
  return conv_layer(image)

image = tf.zeros([1, 200, 200, 100])
# warm up
conv_layer(image); conv_fn(image)

no_tf_fn = timeit.timeit(lambda: conv_layer(image), number=10)
with_tf_fn = timeit.timeit(lambda: conv_fn(image), number=10)
difference = no_tf_fn - with_tf_fn

print("Without tf.function: ", no_tf_fn)
print("With tf.function: ", with_tf_fn)
print("The difference: ", difference)

print("\nJust imagine when we have to do millions/billions of these calculations," \
      " then the difference will be HUGE!")
print("Difference times a billion: ", difference*1000000000)
