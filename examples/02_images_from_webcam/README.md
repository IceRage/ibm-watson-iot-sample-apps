# Sample application for capturing images from webcam and sending them to the IBM Watson IoT Platform

__Dependencies__:

1. Python 2.7.9 ([Link](https://www.python.org/downloads/release/python-279/)).
2. openssl 1.0.1 ([Link](https://www.openssl.org/source/)).
3. ibmiotf 0.2.4 ([Link](https://pypi.python.org/pypi/ibmiotf)).
4. OpenCV including Python bindings 2.4.12 ([Link](http://opencv.org/downloads.html)).

On a Ubuntu machine the dependencies could be installed using:

1. sudo add-apt-repository ppa:fkrull/deadsnakes; sudo apt-get update; sudo apt-get install python2.7 
2. sudo apt-get install openssl
3. sudo pip install ibmiotf
4. sudo apt-get install python-opencv

However before installing these dependencies check that the version of the packages is equal or greater than the versions given above.
