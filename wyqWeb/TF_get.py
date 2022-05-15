import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
def basic_operation():
    v1 = tf.Variable(10)
    v2 = tf.Variable(5)
    addv = v1 + v2
    print(addv)

if __name__ == '__main__':
    basic_operation()
    # print(tf.test.is_gpu_available())
    # print('-----------',tf.test.gpu_device_name())

