FROM ubuntu:16.04
# Update Ubuntu Software repository
RUN apt-get update

# Install pyton
RUN apt-get install -y \
    wget \
    build-essential \
    libz-dev \
    zlib1g-dev \
    curl \
    python-pip \
    software-properties-common \
    python-software-properties \
    python-lxml \
    libboost-program-options-dev \
    libbz2-dev \
    libexpat1-dev \
    cmake \
    pandoc \
    git \
    default-jre \
    default-jdk \
    gradle

# Install node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

# Install Libosmium
RUN git clone https://github.com/mapbox/protozero
RUN cd protozero && git checkout 23d48fd2a441c6e3b2852ff84a0ba398e48f74be && mkdir build && cd build && cmake .. && make && make install
RUN git clone https://github.com/osmcode/libosmium
RUN cd libosmium && git checkout a1f88fe44b01863a1ac84efccff54b98bb2dc886 && mkdir build && cd build && cmake .. && make && make install
RUN git clone https://github.com/osmcode/osmium-tool
RUN cd osmium-tool && git checkout ddbcb44f3ec0c1a8d729e69e3cee40d25f5a00b4 && mkdir build && cd build && cmake .. && make && make install

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

RUN git clone https://github.com/openstreetmap/osmosis.git
WORKDIR osmosis
RUN git checkout 9cfb8a06d9bcc948f34a6c8df31d878903d529fc
RUN mkdir dist
RUN ./gradlew assemble
RUN tar -xvzf "$PWD"/package/build/distribution/*.tgz -C "$PWD"/dist/
RUN ln -s "$PWD"/dist/bin/osmosis /usr/bin/osmosis
RUN osmosis --version 2>&1 | grep "Osmosis Version"

# Copy geokit to container
COPY . .
RUN rm -rf node_modules/ && npm install && npm link
VOLUME /mnt/data
WORKDIR /mnt/data
