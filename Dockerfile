# Use the official Python image for Python 3.11
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS="yes"
ENV PIP_ROOT_USER_ACTION=ignore

ARG USER=proalgotrader
ARG WORKDIR=app

RUN apt-get update && apt-get install -y sudo nano

# Install TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar -xvzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install && cd ..

# Set work directory
WORKDIR /$WORKDIR

# Copy the entire project into the container
COPY ./main.py ./main.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache

# Create user
RUN useradd -m $USER
RUN echo "$USER:$USER" | chpasswd
RUN echo "$USER ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers

# Create file / folder permission for user
RUN chown -R $USER:$USER /$WORKDIR
RUN chmod 755 /$WORKDIR

# Set logged-in user
USER $USER
