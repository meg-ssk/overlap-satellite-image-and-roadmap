# import required modules
import numpy as np
import sys
import cv2
import os

#from shapely.geometry import Point, LineString, Polygon
from osgeo import gdal, osr, ogr

from lib.loader.settings_loader import SettingsDataLoader
from lib.loader.images_downloader import ImageDataDownloader
from lib.processor.image_processor import ImageProcessor

def main():
    """
    python codes to create overlaid satellite image and road map
    """
    # load settings from toml file
    path_to_settings_toml_file = "./settings.toml"
    settings_data_loader = SettingsDataLoader(path_to_settings_toml_file)
    settings = settings_data_loader.load_toml_file()

    # create directories
    os.makedirs(settings.image_download_directory, exist_ok=True)
    os.makedirs(settings.output_image_directory, exist_ok=True)

    # download RGB images
    ImageDataDownloader.image_data_downloader(settings)

    # create and save true color image
    ImageProcessor.create_true_color_image_from_three_bands_images(settings)

    print("Creating road map...")

    # crop San Francisco city from geotiff file
    input_raster_path = settings.output_image_directory + "true_color.tiff"
    output_raster_path = settings.output_image_directory + "San_Francisco.tiff"
    ImageProcessor.crop_geotiff(input_raster_path, output_raster_path, settings)

    # load San Francisco's geotiff raster
    san_francisco_raster = gdal.Open(output_raster_path, gdal.GA_ReadOnly)

    # load road shp file and get layer information as vector
    road_path = "./materials/shp/city-of-san-francisco-california-streets.shp"
    rasterized_road = ImageProcessor.rasterize_shp_file(san_francisco_raster, road_path, settings)

    # create overlap image San Francisco city on road map
    overlap_image_road_on_city = ImageProcessor.overlap_two_raster_images(san_francisco_raster, rasterized_road, settings)
    cv2.imwrite(settings.output_image_directory + "road_map.jpg", overlap_image_road_on_city)

    print("finish!")

if __name__ == "__main__":
    main()