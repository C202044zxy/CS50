import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    # if len(sys.argv) not in [2, 3]:
    #    sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    # images, labels = load_data(sys.argv[1])
    images, labels = load_data()
    # 这里略微修改了一下，直接找到文件夹里的数据读入了，不需要命令行

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    # Attention, we transfrom the labels to one-hot encoded form !
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data():
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # 先找到程序所在的文件夹，然后进入 gtsrb 文件夹
    path = os.path.join(os.getcwd(), "gtsrb")
    images = []
    labels = []
    for i in range(NUM_CATEGORIES):
        # from 0 to 42, loop all categories
        nowpath = os.path.join(path, f"{i}")
        # find all the picture
        lst = os.listdir(nowpath)
        for filename in lst:
            img = cv2.imread(os.path.join(nowpath, filename))
            if img is None:
                raise ValueError
            img = cv2.resize(img, (28, 28), interpolation = cv2.INTER_AREA)
            images.append(img)
            labels.append(i)
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.Sequential([
        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        # 4*4 and 3*3 ---> 2*2 , 卷积的方式还是对应位置相乘再求和
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(28, 28, 3)
        ),
        # Max-pooling layer, using 2x2 pool size
        # 也就是对于每个 2*2 的小矩形求最大值，以这个值代表 2*2 的矩形
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        # Flatten units
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(500, activation = "relu"), 
        # Dropout 是为了防止 overfitting，随机扔掉一些点避免过度依赖某些点
        tf.keras.layers.Dropout(0.5), 
        tf.keras.layers.Dense(NUM_CATEGORIES, activation = "softmax")
    ])
    model.compile(
        optimizer = "adam",
        # labels MUST BE one-hot encoded
        loss = "categorical_crossentropy",
        metrics = ["accuracy"]
    )
    return model

if __name__ == "__main__":
    main()
