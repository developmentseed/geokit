FROM openjdk:11.0.10-buster

RUN apt-get update

# Install pyton
RUN apt-get install -y \
    wget \
    git

# Installing osmosis
RUN git clone https://github.com/openstreetmap/osmosis.git
WORKDIR osmosis
# RUN git checkout 9cfb8a06d9bcc948f34a6c8df31d878903d529fc
RUN mkdir dist
RUN ./gradlew assemble
RUN tar -xvzf "$PWD"/package/build/distribution/*.tgz -C "$PWD"/dist/
RUN ln -s "$PWD"/dist/bin/osmosis /usr/bin/osmosis
RUN osmosis --version 2>&1 | grep "Osmosis Version"

# install aws
RUN apt-get install -y awscli

VOLUME /mnt/data
WORKDIR /mnt/data