import time
import tensorflow as tf

cpu_slot = 0
gpu_slot = 0

# Using CPU at slot 0
with tf.device('/CPU:' + str(cpu_slot)):
    # Starting a timer
    start = time.time()

    # Doing operations on CPU
    A = tf.constant([[3, 2], [5, 2]])
    print(tf.eye(2,2))

    # Printing how long it took with CPU
    end = time.time() - start
    print(end)

with tf.device('/GPU:' + str(gpu_slot)):
    # Starting a timer
    start = time.time()

    # Doing operations on CPU
    A = tf.constant([[3, 2], [5, 2]])
    print(tf.eye(2,2))

    # Printing how long it took with CPU
    end = time.time() - start
    print(end)
