# Use the official Python image for Python 3.11
FROM ghcr.io/krunaldodiya/proalgotrader_core:latest

# Copy the entire project into the container
COPY ./main.py ./main.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache
