import tensorflow as tf

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Income():
    data = pd.read_csv('Income.csv')
    plt.scatter(data.Education,data.Income)
    plt.show()

    x = data.Education
    y = data.Income
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(1,input_shape=(1,)))
    model.summary()
    model.compile(optimizer='adam',loss='mse')
    history = model.fit(x,y,epochs=15000)
    print(model.predict(x))
    print(model.predict(pd.Series([1])))

def Advertising():
    data = pd.read_csv('Advertising.csv')
    # Index(['Unnamed: 0', 'TV', 'Radio', 'Newspaper', 'Sales'], dtype='object')
    plt.scatter(data.Newspaper,data.Sales)
    plt.show()
    x = data.iloc[:,1:-1]
    y = data.iloc[:,-1]
    model = tf.keras.Sequential(
        [tf.keras.layers.Dense(10,input_shape=(3,)),
         tf.keras.layers.Dense(1)
         ]
    )

    model.summary()
    model.compile(optimizer='adam',
                  loss='mse')
    model.fit(x,y,epochs=20000)
    test = data.iloc[:10,1:-1]
    print(model.predict(test))

def credit_a():
    data = pd.read_csv('credit-a.csv',header=None)
    # print(data)
    a = data.iloc[:,-1].value_counts()
    # print(a)
    x = data.iloc[:,:-1]
    y = data.iloc[:,-1].replace(-1,0)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(4,input_shape=(15,),activation='relu'))
    model.add(tf.keras.layers.Dense(4,activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.summary()

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['acc']
    )
    history = model.fit(x,y,epochs=100)
    print(history.history.keys())
    plt.plot(history.epoch,history.history.get('acc'))
    plt.show()

def softmax():
    # fashion_mnist = tf.keras.datasets.fashion_mnist.load_data()
    (train_image,train_lable),(test_image,test_label) = tf.keras.datasets.fashion_mnist.load_data()

    # a = train_image.shape
    # print(a)
    # a = train_lable.shape
    # print(a)
    # a = test_image.shape
    # print(a)
    # a = test_label.shape
    # print(a)

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28,28))) #28*28
    model.add(tf.keras.layers.Dense(128,activation='relu'))
    model.add(tf.keras.layers.Dense(10,activation='softmax'))
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['acc']
    )
    model.fit(train_image,train_lable,epochs=5,batch_size=1)

    print('--------------------')
    print(model.evaluate(test_image,test_label))

if __name__ == '__main__':
    print(tf.test.is_gpu_available())
    exit()
    softmax()