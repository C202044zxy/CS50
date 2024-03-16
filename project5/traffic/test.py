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
print(f"Attention : {train_labels.shape}")

# Flatten 扁平化
# Dense 全连接层
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28, 28)), 
    tf.keras.layers.Dense(128, activation = 'relu'), 
    tf.keras.layers.Dense(10) # corresponding to disceret categories
])
# 要添加：损失函数、优化器、指标
model.compile(optimizer = 'adam', 
              # labels MUST NOT BE one-hot encoded
              loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
              metrics = ['accuracy']
            )
# 先适应训练集
model.fit(train_images, train_labels, epochs = 10)
# 用测试集来评价
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print(f"\nTest accuracy : {test_accuracy}")

# Softmax 可以返回取值的概率
probability_model = tf.keras.Sequential([
    model, 
    tf.keras.layers.Softmax()
])
prediction = probability_model.predict(test_images)
print(prediction[0])