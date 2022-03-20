# base image
FROM ubuntu:20.04

# update
RUN apt-get update && apt-get install -y tzdata
# timezone setting
ENV TZ=Asia/Tokyo

# install python and gdal
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y gdal-bin
RUN apt-get install -y libgdal-dev

# export environment variables
ENV export CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV export C_INCLUDE_PATH=/usr/include/gdal
ENV HOME=/home

# install required libraries from pip
RUN pip3 install numpy opencv-python toml dataclasses requests GDAL==3.0.4 pytest

# copy files
WORKDIR /projects
COPY . /projects