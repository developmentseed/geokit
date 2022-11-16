# Geokit

[![Build Status](https://travis-ci.org/developmentseed/geokit.svg?branch=master)](https://magnum.travis-ci.com/developmentseed/geokit)

Geokit is a command-line interface (CLI) tool written in Javascript and Python, that contains all the basic functionalities for measurements, conversions and operations of geojson files. Furthermore, it also includes some functionalities to process other file formats easily.

Check you the scripts in the language that were written:

- [Node- javascrit ](node-scripts/)
- [Python- javascrit ](python-scripts/)

## CI

To update geokit in docker hub, we use CI with [circleci](https://circleci.com/). To update all three containers at once, we can use a commit in the `develop` branch.

To update containers per technology, we can commit to a branch with the following pattern `<< TECHNOLOGY >>-<< TAG >>`. For instance:

- `python-feature-one`: Will update the `python` container and create a new tag `feature-one`
- `python-develop`: Will update the `python` container and update the `latest` tag. This is a special case, if you want to update the container to `latest`, you can use `develop` in the branch name.
