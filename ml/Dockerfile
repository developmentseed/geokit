FROM python:3.7
LABEL maintainer "developmentseed"



# Copy geokit to container
RUN mkdir ml-scripts
WORKDIR /ml-scripts
ADD requirements.txt /ml-scripts/
RUN pip install --no-cache-dir -r requirements.txt

ADD . /ml-scripts/

