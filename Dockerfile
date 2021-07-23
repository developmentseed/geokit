FROM ubuntu:16.04
LABEL maintainer "developmentseed"

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
    gradle \
    libsqlite3-dev

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

# Install editors
RUN apt-get install -y nano vim

# Install to download osm data for a polygon
RUN git clone https://github.com/Rub21/dosm.git && cd dosm && npm i && npm link

# Install osm-obj-counter
RUN git clone https://github.com/developmentseed/osm-obj-counter.git && cd osm-obj-counter && npm i && npm link

# Installing osmosis
RUN git clone https://github.com/openstreetmap/osmosis.git
WORKDIR osmosis
RUN git checkout 9cfb8a06d9bcc948f34a6c8df31d878903d529fc
RUN mkdir dist
RUN ./gradlew assemble
RUN tar -xvzf "$PWD"/package/build/distribution/*.tgz -C "$PWD"/dist/
RUN ln -s "$PWD"/dist/bin/osmosis /usr/bin/osmosis
RUN osmosis --version 2>&1 | grep "Osmosis Version"

# Installing minjur
RUN mkdir /mason
WORKDIR /mason
RUN curl -sSfL https://github.com/mapbox/mason/archive/v0.6.0.tar.gz | \
    tar --gunzip --extract --strip-components=1 --directory=./
RUN ./mason install minjur 0.1.0
RUN ./mason link minjur 0.1.0
RUN ./mason_packages/.link/bin/minjur --version
RUN ln ./mason_packages/.link/bin/minjur /usr/bin/minjur
RUN ln ./mason_packages/.link/bin/minjur-mp /usr/bin/minjur-mp
RUN ln ./mason_packages/.link/bin/minjur-generate-tilelist /usr/bin/minjur-generate-tilelist

# Installing tippecanoe
RUN git clone https://github.com/mapbox/tippecanoe.git /tmp/tippecanoe-src
WORKDIR /tmp/tippecanoe-src
RUN git checkout 610afc23329d3674f5bb2561bfd027653d3004a9
RUN make && make install

# Install osmconv
RUN git clone https://github.com/developmentseed/osm-coverage-tiles.git
RUN cd osm-coverage-tiles && git checkout -b 63ff18169bc7bf9e6ee253f26bc2f4e855d59af6 && npm install && npm link

# Install PIP
RUN curl https://bootstrap.pypa.io/2.7/get-pip.py --output get-pip.py 
RUN python get-pip.py

# Install csvkit
RUN git clone -b 1.0.4 --depth=1 https://github.com/wireservice/csvkit.git && cd csvkit && pip install -r requirements-py2.txt && python setup.py install

# Install mbtiles extractor
RUN git clone https://github.com/mapbox/mbtiles-extracts.git && cd mbtiles-extracts && npm link

# Install modules for processing images
RUN apt-get -y install libjpeg-dev libpng-dev
RUN pip install lycon

# Install csv2geojson
RUN npm install -g csv2geojson

# Install Mapbox cli
RUN pip install mapboxcli

# Copy geokit to container
RUN mkdir /geokit
WORKDIR /geokit
COPY . .
RUN rm -rf node_modules/ && npm install && npm link
VOLUME /mnt/data
WORKDIR /mnt/data