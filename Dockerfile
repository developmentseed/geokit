FROM ubuntu:16.04
# Update Ubuntu Software repository
RUN apt-get update

# Install pyton
RUN apt-get install -y \
    wget \
    build-essential \
    libz-dev \
    zlib1g-dev \
    git \
    curl \
    python-pip \
    software-properties-common \
    python-software-properties \
    python-lxml \
    libboost-program-options-dev \
    libbz2-dev zlib1g-dev \
    libexpat1-dev \
    cmake \
    pandoc \
    git

# Install node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

# Install Libosmium
RUN git clone https://github.com/mapbox/protozero
RUN cd protozero && mkdir build && cd build && cmake .. && make && make install
RUN git clone https://github.com/osmcode/libosmium
RUN cd libosmium && mkdir build && cd build && cmake .. && make && make install
RUN git clone https://github.com/osmcode/osmium-tool
RUN cd osmium-tool && mkdir build && cd build && cmake .. && make && make install

# Other node libraries from https://github.com/node-geojson
RUN npm install -g osmtogeojson
RUN npm install -g geojsontoosm
RUN npm install -g geojson2poly 
RUN npm install -g geojson-pick
RUN npm install -g @mapbox/geojson-merge

# Install osmconvert and osmfilter
RUN wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert
RUN cp osmconvert /usr/bin/osmconvert
RUN wget -O - http://m.m.i24.cc/osmfilter.c |cc -x c - -O3 -o osmfilter
RUN cp osmfilter /usr/bin/osmfilter

# install editors
RUN apt-get install -y nano vim

# Install to download osm data for a polygon
RUN git clone https://github.com/Rub21/dosm.git && cd dosm && npm i && npm link

# Install osm-obj-counter
RUN git clone https://github.com/developmentseed/osm-obj-counter.git && cd osm-obj-counter && npm i && npm link

# Copy geokit to container
COPY . .
RUN rm -rf node_modules/ && npm install && npm link
WORKDIR app/
RUN mkdir data/
# CMD [ "geokit" ]