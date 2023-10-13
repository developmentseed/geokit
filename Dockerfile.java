FROM openjdk:17-jdk-buster

# Install pyton
RUN apt-get update && apt-get install -y \
    wget \
    git \
    osmosis


VOLUME /mnt/data
WORKDIR /mnt/data