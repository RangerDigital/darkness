FROM ubuntu:latest
RUN apt update

# Install Python 3, Gunicorn.
RUN apt install -y python3 python3-pip gunicorn3

# Install dependencies.
RUN pip3 install flask
RUN pip3 install rpi-ws281x

# Copy files.
COPY darkness/* /

# Run app server.
CMD gunicorn3 -b 0.0.0.0:8000 app:app
