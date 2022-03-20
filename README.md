# READ ME

## Purpose
The codes included in this repositry can generate
1. True color image from Landsat8 images of three bands.
1. Overlaid satellite image and road map of San-Francisco city.

The Landsat8 images are downloaded automatically via AWS by running the code.

## How to install?
Perform below on your terminal (Make sure Docker is installed and running).
```bash
docker build --tag landsat8 .
```

## How to run?
Run the python code by the following command:
```bash
docker run --rm -m 8G -it landsat8 python3 src/main.py
```


## How to perform unit test?
You can perform unit test by pytest as:
```bash
docker run --rm -m 8G -it landsat8 pytest tests
```

## Copy the result images in container to your local host
Copy the results in the container to the local host and look at the results:
```bash
docker cp <container ID>:/projects  <full path to your directory>
```


## Where is generated image?
After the code has finished running, the results images will be saved in the following directory.
```bash
./output-images
```
In addition to the two desired jpg images, some geotiff images will also be generated.
These geotiff images will be useful to see by GIS software such as QGIS.



## How to obtain Landsat8 images?
The default setting　will download Landsat8 images via AWS from the following url:  
https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/044/034/LC08_L1TP_044034_20190706_20190706_01_RT/index.html  
When you run the code, images will be downloaded automatically to 
```bash
./materials/images/
```
If you would like to change the image to download, please edit first line of `. /settings.toml`.
```bash
scene_url = "https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/044/034/LC08_L1TP_044034_20190706_20190706_01_RT/index.html"
```
To get the AWS url, please refer to the following sites:  
https://github.com/awslabs/open-data-docs/tree/main/docs/landsat-pds
https://earthexplorer.usgs.gov

## How did we get the road map data?
The shp file of road map in San-Francisco city was acquired from:  
https://koordinates.com/layer/101761-city-of-san-francisco-california-streets/  
Please put unzipped files to the directory : `./materials/shp/`

## What is 'settings.toml'?
Several parameters required for the analysis can be changed from this file.
```bash
scene_url = "https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/044/034/LC08_L1TP_044034_20190706_20190706_01_RT/index.html"
image_download_directory = "./materials/images/"
output_image_directory = "./output-images/"
EPSG = 32610
crop_area = [542645, 4184720, 554019, 4176372]
```
- `scene_url` is the AWS url of the image to download.
- `image_download_directory` is the directory where Landsat8 images will be downloaded.
- `output_image_directory` is the rirectory where　the processed images will be saved.
- `EPSG` is the EPSG code of downloaded Landsat8 images. Edit here according to the coordinate system of the image you download.
- `crop_area` are the coordinates of the 4 vertices for cropping a specific area (in this case, San Francisco) as: `[xmin, ymin, xmax, ymax]`. Please set it according to the coordinate system of EPSG and the region of interest.

## Known issues
1. `src/lib/loader/image_downloader.py` is the code that downloads the Landast images, but I don't have godd idea how to properly unit test it.
1. I also tried to create an image using a histogram equalization.
The true color image generated by histogram equalization is saved `./output-images/tci_hist_eq.jpg`. Please see the image for reference.
I think we need to do more to make more natural coloring.

## References
1.  https://github.com/awslabs/open-data-docs/tree/main/docs/landsat-pds
1. https://www.usgs.gov/media/images/landsat-8-band-designations
1. https://earthexplorer.usgs.gov
1. https://koordinates.com/layer/101761-city-of-san-francisco-california-streets/
1. https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_equalize.html#sphx-glr-auto-examples-color-exposure-plot-equalize-py
1. https://stackoverflow.com/questions/38242716/how-to-crop-a-raster-image-by-coordinates-in-python
