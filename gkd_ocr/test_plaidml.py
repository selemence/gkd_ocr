import os
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import load_model

characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
characters += '一二三四五六七八九十百千万亿'  # 常见的中文字符

# 创建字符到索引的映射
char_to_index = {char: i for i, char in enumerate(characters)}
index_to_char = {i: char for i, char in enumerate(characters)}

# 数据路径
image_dir = 'data/images'
label_dir = 'data/labels'

# 读取所有标签文件，收集所有出现的字符
def collect_characters(label_dir):
    all_chars = set(characters)
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            label_path = os.path.join(label_dir, filename)
            with open(label_path, 'r') as f:
                label_str = f.read().strip()
                for char in label_str:
                    all_chars.add(char)
    return all_chars

# 更新字符集
def update_characters(all_chars):
    new_characters = ''.join(sorted(all_chars))
    new_char_to_index = {char: i for i, char in enumerate(new_characters)}
    new_index_to_char = {i: char for i, char in enumerate(new_characters)}
    return new_characters, new_char_to_index, new_index_to_char

# 收集所有字符
all_chars = collect_characters(label_dir)
new_characters, new_char_to_index, new_index_to_char = update_characters(all_chars)

# 更新字符集和映射
characters = new_characters
char_to_index = new_char_to_index
index_to_char = new_index_to_char

# 计算类别数
num_classes = len(characters)
print(f"更新后的字符集: {characters}")
print(f"更新后的字符到索引的映射: {char_to_index}")
print(f"更新后的索引到字符的映射: {index_to_char}")
print(f"更新后的类别数: {num_classes}")

# 数据路径
image_dir = 'data/images'
label_dir = 'data/labels'

# 加载数据
def load_data(image_dir, label_dir, image_size=(100, 30), num_classes=num_classes):
    images = []
    labels = []
    for filename in os.listdir(image_dir):
        if filename.endswith('.png'):
            # 加载图像
            img_path = os.path.join(image_dir, filename)
            img = load_img(img_path, target_size=image_size, color_mode='grayscale')
            img_array = img_to_array(img) / 255.0
            images.append(img_array)

            # 加载标签
            label_path = os.path.join(label_dir, filename.replace('.png', '.txt'))
            with open(label_path, 'r') as f:
                label_str = f.read().strip()
                label = [char_to_index[char] for char in label_str]
                label = to_categorical(label, num_classes=num_classes)
                labels.append(label)

    return np.array(images), np.array(labels)

# 加载数据
X, y = load_data(image_dir, label_dir)

# 构建模型
def build_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes * 4, activation='softmax'))  # 假设验证码长度为4

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 模型参数
input_shape = (100, 30, 1)  # 图像尺寸 (高度, 宽度, 通道数)

# 构建模型
model = build_model(input_shape, num_classes)

# 训练模型
model.fit(X, y, batch_size=32, epochs=10, validation_split=0.2)

# 保存模型
model.save('captcha_model.h5')

# 加载模型
model = load_model('captcha_model.h5')

# 预测
def predict_image(image_path, model, image_size=(100, 30)):
    img = load_img(image_path, target_size=image_size, color_mode='grayscale')
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_labels = np.argmax(predictions, axis=-1)
    predicted_label_str = ''.join([index_to_char[i] for i in predicted_labels[0]])
    return predicted_label_str

# 预测示例
image_path = 'data/images/example.png'
predicted_label = predict_image(image_path, model)
print(f'Predicted label: {predicted_label}')