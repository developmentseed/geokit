FROM ubuntu:16.04
# Update Ubuntu Software repository
RUN apt-get update
# Install pyton
RUN apt-get install -y wget build-essential libz-dev zlib1g-dev git curl python-pip software-properties-common python-software-properties python-lxml
# Install node
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
# Clone geokit repo
RUN git clone https://github.com/developmentseed/geokit.git && cd geokit && npm link
RUN mkdir -p app
WORKDIR app/
