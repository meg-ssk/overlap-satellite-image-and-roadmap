import sys
sys.path.append('./')
from src.lib.loader.settings_loader import SettingsData, SettingsDataLoader
from src.lib.processor.image_processor import ImageProcessor
import pytest
import numpy as np
import cv2
from osgeo import gdal, osr, ogr

# load settings and modify outout directory fotr test
settings = SettingsDataLoader('./settings.toml').load_toml_file()
settings.output_image_directory = "./tests/test_images/"

def test_create_true_color_image_from_three_bands_images():
    ImageProcessor.create_true_color_image_from_three_bands_images(settings)
    
    true_color_image_solution = cv2.imread("./output-images/tci.jpg")
    true_color_image_test = cv2.imread(settings.output_image_directory + "tci.jpg")

    res = (true_color_image_solution == true_color_image_test).all()

    assert res


def test_crop_geotiff():
    input_raster_path = settings.output_image_directory + "true_color.tiff"
    output_raster_path = settings.output_image_directory + "San_Francisco.tiff"

    ImageProcessor.crop_geotiff(input_raster_path, output_raster_path, settings)

    crop_image_solution = gdal.Open("./output-images/San_Francisco.tiff").ReadAsArray()
    crop_image_test     = gdal.Open(settings.output_image_directory + "San_Francisco.tiff").ReadAsArray()

    res = (crop_image_solution == crop_image_test).all()
    assert res


def test_rasterize_shp_file():
    under_image = gdal.Open(settings.output_image_directory + "San_Francisco.tiff", gdal.GA_ReadOnly)
    shp_path = "./materials/shp/city-of-san-francisco-california-streets.shp"
    
    rasterize_shp_arr = ImageProcessor.rasterize_shp_file(under_image, shp_path, settings)

    rasterise_shp_solution = gdal.Open("./output-images/road.tiff").ReadAsArray()
    rasterise_shp_test = gdal.Open(settings.output_image_directory + "road.tiff").ReadAsArray()

    np.save('./tests/test_npy/rasterized_road', rasterize_shp_arr)

    res = (rasterise_shp_solution == rasterise_shp_test).all()
    assert res


def test_overlap_two_raster_images():
    san_francisco_raster = gdal.Open(settings.output_image_directory + "San_Francisco.tiff")
    rasterized_road = np.load('./tests/test_npy/rasterized_road.npy')

    overlap_image = ImageProcessor.overlap_two_raster_images(san_francisco_raster, rasterized_road, settings)
    cv2.imwrite("." + settings.output_image_directory + "map.jpg", overlap_image)

    overlap_image_solution = cv2.imread("./output-images/map.jpg")
    overlap_image_test     = cv2.imread("./tests/test_images/map.jpg")

    res = (overlap_image_solution == overlap_image_test).all()
    assert res


def test_histogram_equalization_except_zero():
    image_org = cv2.imread("./tests/test_images/hist_eq_before.png", 0)
    image_hust_eq_after = cv2.imread("./tests/test_images/hist_eq_after.png", 0)

    image_hist_eq_test = ImageProcessor.histogram_equalization_except_zero(image_org, 255)

    res = (image_hust_eq_after == image_hist_eq_test).all()

    assert res