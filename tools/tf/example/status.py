import tensorflow as tf

if(tf.executing_eagerly()):
    print('Eager execution is enabled (running operations immediately)\n')
    print(('Turn eager execution off by running: \n{0}\n{1}').format('' \
        'from tensorflow.python.framework.ops import disable_eager_execution', \
        'disable_eager_execution()'))
else:
    print('You are not running eager execution. TensorFlow version >= 2.0.0' \
          'has eager execution enabled by default.')
    print(('Turn on eager execution by running: \n\n{0}\n\nOr upgrade '\
           'your tensorflow version by running:\n\n{1}').format(
           'tf.compat.v1.enable_eager_execution()',
           '!pip install --upgrade tensorflow\n' \
           '!pip install --upgrade tensorflow-gpu'))

print(('Is your GPU available for use?\n{0}').format(
    'Yes, your GPU is available: True' if tf.test.is_gpu_available() == True else 'No, your GPU is NOT available: False'
))

print(('\nYour devices that are available:\n{0}').format(
    [device.name for device in tf.config.experimental.list_physical_devices()]
))
