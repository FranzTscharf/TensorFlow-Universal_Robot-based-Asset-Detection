FROM ubuntu:14.04
COPY ./bin /
MAINTAINER Viktor Walter-Tscharf
RUN apt-get update && apt-get -y install zbar-tools && apt-get -y install python && apt-get clean
RUN apt-get -y install python-setuptools
RUN sudo easy_install pip
RUN pip install imutils
RUN pip install numpy
RUN pip install opencv-python
