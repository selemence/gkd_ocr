import numpy as np

def convolution_2d(input_matrix, kernel):
    input_h, input_w = input_matrix.shape
    kernel_h, kernel_w = kernel.shape
    output_h = input_h - kernel_h + 1
    output_w = input_w - kernel_w + 1
    output_matrix = np.zeros((output_h, output_w))
    
    for i in range(output_h):
        for j in range(output_w):
            region = input_matrix[i:i + kernel_h, j:j + kernel_w]
            output_matrix[i, j] = np.sum(region * kernel)
    
    return output_matrix

input_matrix = np.array([
    [1, 2, 1, 1],
    [5, 7, 9, 2],
    [4, 6, 8, 3],
    [3, 5, 6, 1]
])

kernel = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
])

result = convolution_2d(input_matrix, kernel)
print("Convolution result:")
print(result)
