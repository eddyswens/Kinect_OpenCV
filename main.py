#!/usr/bin/env python
import freenect
import cv2
import frame_convert_cv2
import numpy as np

# kinect params
threshold = 100  # глубина (как далеко видит)
current_depth = 0  # точка глубины (откуда начинает видеть)

# pixel resize params:
ratio = 640/480
h = 300
w = int(h * ratio)


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def change_pixels_num(value):
    global w, h
    if value != 0:
        h = value
        w = int(h * ratio)


def resize_frame(frame):
    height, width = frame.shape[:2]

    # Resize input to "pixelated" size
    temp = cv2.resize(frame, (w, h), interpolation=cv2.INTER_NEAREST)

    # Initialize output image
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    return output


def show_depth():
    global threshold
    global current_depth

    # получение кадра глубины, преобразование в двочиную матрицу, преобразование в нужный тип
    depth, timestamp = freenect.sync_get_depth()
    depth_binary = np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
    depth_binary = depth_binary.astype(np.uint8)

    # масштабирование двоичной матрицы
    depth_binary_matrix = cv2.resize(depth_binary, (w, h), interpolation=cv2.INTER_LINEAR)
    print(depth_binary_matrix)

    # Двойное масштабирование для корректного отображения
    output = resize_frame(255 * depth_binary)

    cv2.imshow('Depth', output)


def show_video():
    cv2.imshow('Video', frame_convert_cv2.video_cv(freenect.sync_get_video()[0]))


# creating app
cv2.namedWindow('Depth')
cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)
cv2.createTrackbar('num of pixels in h',     'Depth', h, 640, change_pixels_num)

print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    if cv2.waitKey(10) == 27:
        break
