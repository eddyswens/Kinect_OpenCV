Порядок уставноки библиотеки на Python (https://openkinect.org/wiki/Python_Wrapper):
(В оригинале библиотека написана на C++)

1) Уставноить зависимости:
sudo apt install cython3
sudo apt install python3-dev
sudo apt install python3-numpy
sudo apt install pip
pip install opencv-python

2) Устанавливаем пакет для Ubuntu (https://openkinect.org/wiki/Getting_Started#Official_packages):
sudo apt install freenect
2.1) Проверить уставноку можно командой:
freenect-glview

3) Скачать репозиторий библиотеки (предварительно выбрав нужную папку под это дело):
git clone https://github.com/OpenKinect/libfreenect.git

4) Переместиться в директорию:
cd libfreenect/wrappers/python

5) Запустить установочник wrapper-а:
sudo python3 setup.py install
В итоге получим собранную библиотеку на python, путь до которой отобразится в терминале.

6) Для корректной работы рекомендуется:
sudo modprobe gspca_kinect

7) Сделать перезагрузку/логаут

