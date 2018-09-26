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
    python-lxml

# Install node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

RUN npm install -g @mapbox/geojson-merge
RUN npm install -g osmtogeojson
RUN npm install -g geojsontoosm
RUN npm install geojson2poly -g

COPY . .
RUN rm -rf node_modules/
RUN npm install
RUN npm link
WORKDIR app/