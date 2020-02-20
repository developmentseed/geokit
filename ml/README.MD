# Geokit-ml


Geokit-ml is a command-line interface (CLI) tool written in python3, that contains all the basic functionalities for measurements, conversions and operations of geojson files.


# Usage

# Downsized images

Add all the images that you want to downsize in a folder, supports `jpg` files and the files will be resized to `512X512`.

```
 docker run --rm -v ${PWD}:/mnt/data developmentseed/geokit:latest geokit downsized-imgs <FOLDER>
```

