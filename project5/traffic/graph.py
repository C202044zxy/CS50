import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# load data
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
# [0,9] corresponding to a category of objects
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
train_images = train_images / 255.0
test_images = test_images / 255.0

# check the image
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

# try to use subplot
plt.figure(figsize=(10, 10))
for i in range(25):
    # 将图层分为 5*5 的部分，当前图片在编号为 i 的位置，左上角编号为 1
    plt.subplot(5, 5, i+1)
    plt.xticks([]) # 原来是设置刻度的函数
    plt.yticks([]) # 传空列表相当于禁用刻度
    plt.imshow(train_images[i], cmap = 'gray')
    plt.xlabel(class_names[train_labels[i]])
plt.show()