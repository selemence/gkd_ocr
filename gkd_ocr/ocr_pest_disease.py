import os
import cv2
import numpy as np
import plaidml.keras
plaidml.keras.install_backend()
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical

# 数据预处理
def preprocess_image(image_path, target_size=(128, 128)):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return None  
    image = cv2.resize(image, target_size)
    image = image / 255.0
    return image

def load_images(dataset_path, targe=(128, 128)):
    x_train = []
    y_train = []
    class_names = os.listdir(dataset_path)
    class_to_index = {class_name: i for i, class_name in enumerate(class_names)}
    class_name = ''
    for name1 in class_names:
        class_name = name1
    for image_name in os.listdir(dataset_path):
        image_path = os.path.join(dataset_path, image_name)
        if os.path.isfile(image_path):
            image = preprocess_image(image_path, targe)
            x_train.append(image)
            y_train.append(class_to_index[class_name])
    
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    
    print(f"Loaded {len(x_train)} images from {dataset_path}")
    print(f"x_train shape: {x_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    return x_train, y_train, class_names

x_train, y_train, class_names = load_images('gkd_ocr\\dataset\\train')
x_test, y_test, _ = load_images('gkd_ocr\\dataset\\test')
x_val, y_val, _ = load_images('gkd_ocr\\dataset\\val')

y_train = to_categorical(y_train, num_classes=len(class_names))
y_val = to_categorical(y_val)
y_test = to_categorical(y_test)


model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(class_names), activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
print('模型准备训练')

history = model.fit(x_train, y_train, batch_size=32,
                    steps_per_epoch=len(x_train) // 32,
                    epochs=10,
                    validation_data=(x_val, y_val))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test accuracy:', score[1])
model.save('wheat_pest_disease_model.h5')

from keras.models import load_model

model = load_model('wheat_pest_disease_model.h5')
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test, axis=1)
print('Predicted classes:', predicted_classes)
print('True classes:', true_classes)