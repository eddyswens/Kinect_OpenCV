#!/usr/bin/env python
import freenect
import cv2
import frame_convert_cv2
import numpy as np
import proto


# kinect params
threshold = 100  # глубина (как далеко видит)
current_depth = 800  # точка глубины (откуда начинает видеть)

# pixel resize params:
ratio = 480/480
h = 15
w = int(h * ratio)

#Gauss_Blur
k_size = 59  #ВАЖНО!!! Только нечетные значения
sigX_size = 0


stream = proto.SerialStream("/dev/ttyACM0", 230400)
messenger = proto.Messenger(stream)
hub = messenger.hub
for i in range(5):
    connected = hub.connect()
    if connected:
        print("connected")
        break
if (not connected):
    print("connectionFail")


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

def change_gauss_kernel(value):  # должно быть нечетным
    global k_size
    if value % 2 != 0:
        k_size = value


def change_gauss_sigX(value):
    global sigX_size
    sigX_size = value


def pixelate_frame_view(frame):
    height, width = frame.shape[:2]

    # Resize input to "pixelated" size
    temp = cv2.resize(frame, (w, h), interpolation=cv2.INTER_NEAREST)

    # Initialize output image
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    return output


def crop(arr, f, t):
    return arr[:, f:t]


def filter_gauss(arr):
    return cv2.GaussianBlur(arr, (k_size, k_size), sigX_size)


def mat_to_binary_mask(arr):
    outputmask = 0
    # h = np.shape(arr)[0]
    # w = np.shape(arr)[1]

    for i in range(15):
        for j in range(15):
            if arr[i][j] == 1:
                outputmask |= 1 << (i * 15 + j)

    return outputmask


def show_depth():
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()  # Получение кадра глубины, преобразование в двочиную матрицу, преобразование в нужный тип
    cropped_depth = crop(depth, 80, 560) # Обрезать по ширине от и до

    depth_binary = np.logical_and(cropped_depth >= current_depth - threshold, cropped_depth <= current_depth + threshold)
    depth_binary = depth_binary.astype(np.uint8)
    filtered_depth_binary = filter_gauss(depth_binary)

    depth_binary_matrix = cv2.resize(filtered_depth_binary, (w, h), interpolation=cv2.INTER_LINEAR)  # масштабирование двоичной матрицы
    flipped_depth = np.flip(depth_binary_matrix, axis=1)
    print(depth_binary_matrix)
    binary_mask = mat_to_binary_mask(flipped_depth)  # перевод в двоичную маску

    # Двойное масштабирование для корректного отображения
    output = pixelate_frame_view(255 * filtered_depth_binary)

    cv2.imshow('Depth', output)

    return binary_mask


def show_video():
    cv2.imshow('Video', frame_convert_cv2.video_cv(freenect.sync_get_video()[0]))


# creating app
cv2.namedWindow('Depth')
# cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)
cv2.createTrackbar('num of pixels', 'Depth', h, 640, change_pixels_num)
cv2.createTrackbar('Gauss Kernel',  'Depth', k_size, 100, change_gauss_kernel)
cv2.createTrackbar('Gauss Sigma X', 'Depth', sigX_size, 100, change_gauss_sigX)

print('Press ESC in window to stop')

while 1:
    outputmask = show_depth()
    show_video()

    # Преобразование битовой маски в последовательность байтов
    bytes_num = (outputmask.bit_length() + 7) // 8
    bytes_data = outputmask.to_bytes(bytes_num, byteorder='little')
    if bytes_data == b'':
        bytes_data = b'\x00'
    new_bytes_data = bytearray(32)  # Создаем новый bytearray размером в 32 байт
    new_bytes_data[
    :bytes_num] = bytes_data  # Заполняем первые bytes_num элементов нового bytearray элементами из bytes
    sync_bytes = bytes([0xf5, 0xe4, 0x77])

    common_color = bytes([0x11, 0x11, 0x11])
    custom_data = bytes([0, 0, 0, 0, 0])
    hub.components[0].writeRadio(sync_bytes + common_color + custom_data + bytes(new_bytes_data))

    if cv2.waitKey(50) == 27:
        break


#TODO:
#DONE: Обрезать по раям до квадрата, Применить фильтр Гауса/еще что то, преобразовать массив в двоичное число