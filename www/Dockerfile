# A simple Flask app container.
FROM python:2.7
MAINTAINER Ashay Argal <ashay_argal@sjsu.edu>

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip install -r requirements.txt

EXPOSE 5000
CMD python index.py
