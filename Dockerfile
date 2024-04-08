FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# install python
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.8

# ENV TZ=Europe/London

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
  software-properties-common \
  build-essential \
  curl \
  ffmpeg \
  git \
  vim \
  nano \
  rsync \
  wget \
  unzip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

  RUN add-apt-repository ppa:deadsnakes/ppa
  RUN apt-get update && apt-get install -y -qq python${PYTHON_VERSION} \
      python${PYTHON_VERSION}-dev \
      python${PYTHON_VERSION}-distutils \
      python${PYTHON_VERSION}-tk

# Set python aliases
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py

EXPOSE 8888

# default workdir
WORKDIR /home/workdir
COPY . .

RUN pip install wheel && \
    pip install -r ./requirements.txt && \
    pip install pogema 

# RUN wget https://raw.githubusercontent.com/oxwhirl/pymarl/master/install_sc2.sh && \
    # bash install_sc2.sh

RUN git config --global --add safe.directory /home/workdir

CMD ["/bin/bash"]