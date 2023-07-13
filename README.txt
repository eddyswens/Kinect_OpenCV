Порядок уставноки библиотеки на Python (https://openkinect.org/wiki/Python_Wrapper):
(В оригинале библиотека написана на C++)

1) Уставноить зависимости:
sudo apt-get install cython3
sudo apt-get install python3-dev
sudo apt-get install python3-numpy
sudo pip install opencv-python

2) Скачать репозиторий библиотеки (предварительно выбрав нужную папку под это дело):
git clone https://github.com/OpenKinect/libfreenect.git

3) Переместиться в директорию:
cd libfreenect/wrappers/python

4) Запустить установочник wrapper-а:
sudo python setup.py install

В итоге получим собранную библиотеку на python, путь до которой отобразится в терминале.



Порядок уставноки пакета для Ubuntu (https://openkinect.org/wiki/Getting_Started#Official_packages):

1) Прописываем:
sudo apt-get install freenect

2)Проверить уставноку можно командой:
freenect-glview