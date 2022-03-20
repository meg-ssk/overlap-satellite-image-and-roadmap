import sys
from osgeo import gdal, osr, ogr
import numpy as np
import cv2

class ImageProcessor:
    @classmethod    
    def create_true_color_image_from_three_bands_images(cls, settings):
        """
        create true color images from red, green, and blue images.

        input: 
        settings (dataclass)
            pre-defined parameters, we need directory where landsat images are saved.
        output:
            true color image "true_color_image.jpg" will be created in the directory set by settings
        """
        print("creating true color image...")

        # read geotiff files
        image_red = gdal.Open(settings.image_download_directory + "red.tiff")
        image_green = gdal.Open(settings.image_download_directory + "green.tiff")
        image_blue = gdal.Open(settings.image_download_directory + "blue.tiff")

        # read geo reference information
        geo_transform = image_blue.GetGeoTransform()
        projection = image_blue.GetProjection()

        # convert to ndarray
        image_red_arr = image_red.ReadAsArray()
        image_green_arr = image_green.ReadAsArray()
        image_blue_arr = image_blue.ReadAsArray()

        # write as geotiff file
        rows, cols = image_red_arr.shape
        band, dtype = 3, gdal.GDT_Int32
        output_geotiff = gdal.GetDriverByName("GTiff").Create(settings.output_image_directory + 
                                                              "true_color.tiff", cols, rows, band, dtype, options = ['PHOTOMETRIC=RGB'])
        # append geo reference information
        EPSG = settings.EPSG
        output_geotiff.SetGeoTransform(geo_transform)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(EPSG)
        output_geotiff.SetProjection(srs.ExportToWkt())

        # write each color as band
        output_geotiff.GetRasterBand(1).WriteArray(image_red_arr)
        output_geotiff.GetRasterBand(2).WriteArray(image_green_arr)
        output_geotiff.GetRasterBand(3).WriteArray(image_blue_arr)

        # save as geotiff
        output_geotiff.FlushCache()

        # save as jpg
        output_arr = output_geotiff.ReadAsArray()
        output_arr = output_arr[:,:,::-1] # convert RGB to BGR
        output_arr = np.transpose(output_arr)
        output_arr = cv2.rotate(output_arr, cv2.ROTATE_90_CLOCKWISE) # rotate
        #output_arr = cv2.flip(output_arr, 0) # flip

        #print("Histogram equalization is performed...")

        """
        normarize_constant = np.max([np.max(image_red_arr), np.max(image_green_arr), np.max(image_blue_arr)])
        for i in range(0,3):
            output_arr[:,:,i]  = cls.histogram_equalization_except_zero(output_arr[:,:,i],  normarize_constant)
        """

        # set the maximum value to 255
        for i in range(0,3):
            output_arr[:,:,i]  = (output_arr[:,:,i]/np.max(output_arr)*255).astype(np.uint8)

        # convert RGB to BGR
        output_arr = output_arr[:, :, ::-1]

        # write the image
        cv2.imwrite(settings.output_image_directory + "true_color_image.jpg", output_arr)

        output_geotiff = None

        return 
    

    @classmethod
    def crop_geotiff(cls, input_raster_path, output_raster_path, settings):
        """
        crop a part of the geotiff image
        (in this case, we will focus on San Francisco city)

        input: 
        input_raster_path (str):
            path to geotiff image before cropping.
        output_raster_path (str):
            path to geotiff image after cropping.
        settings (dataclass)
            pre-defined parameters.
            we need directory where output images are saved and coordinates of 4 vertices for croppring.
        
        output:
            croped geotiff image will be created in the directory set by output_raster_path
        """
        bbox = tuple(settings.crop_area)
        raster = gdal.Open(input_raster_path)
        gdal.Translate(output_raster_path, input_raster_path, projWin = bbox)

        return
    

    @classmethod
    def rasterize_shp_file(cls, input_raster_image, vector_data_path, settings):
        """
        create true color images from red, green, and blue images.

        input: 
        input_raster_image (gdal):
            geotiff image oped by gdal
        vector_data_path:
            path to vector data (e.g. shp file) which will be rasterized.
        settings (dataclass)
            pre-defined parameters, we need directory where output images are saved.
        
        output:
            croped geotiff image will be created in the directory set by output_raster_path
        """

        # load geotiff image
        output_raster_image_path = settings.output_image_directory + "road.tiff"
        band, dtype = 3, gdal.GDT_Int32
        output_raster_image = gdal.GetDriverByName("GTiff").Create(output_raster_image_path,
                                                                   input_raster_image.RasterXSize,
                                                                   input_raster_image.RasterYSize,
                                                                   band, dtype, options=['COMPRESS=DEFLATE'])
        # get geo reference information
        output_raster_image.SetProjection(input_raster_image.GetProjectionRef())
        output_raster_image.SetGeoTransform(input_raster_image.GetGeoTransform())

        # rasterize shp file data
        gdal.Rasterize(output_raster_image, vector_data_path, burnValues=[255,255,255])

        # arange the nd array
        output_raster_image_arr = output_raster_image.ReadAsArray()
        output_raster_image_arr = np.transpose(output_raster_image_arr)
        output_raster_image_arr = cv2.rotate(output_raster_image_arr, cv2.ROTATE_90_COUNTERCLOCKWISE) # rotate
        output_raster_image_arr = cv2.flip(output_raster_image_arr, 0) # flip

        output_raster_image = None

        return output_raster_image_arr

    @classmethod
    def overlap_two_raster_images(cls, under_image, over_image_arr, settings):
        """
        overlap two raster images.
        here, under image is San Francisco city, overlaid image is road map.

        input: 
        under_image (gdal):
            geotiff image oped by gdal.
            another image will be overlapped on this image.
        over_image_arr (ndarray):
            image (ndarray) that will be overlaid on under image.
            here, it means road map 
        settings (dataclass)
            pre-defined parameters, we need directory where output images are saved.
        
        output:
        overlaped_image(ndarray):
            image (ndarray) of San Francisco with road map overlapped.
        """
        transparence_color = (0,0,0)

        # arange geotiff image as nd array
        under_raster_image_arr = under_image.ReadAsArray()
        under_raster_image_arr = np.transpose(under_raster_image_arr)
        under_raster_image_arr = cv2.rotate(under_raster_image_arr, cv2.ROTATE_90_COUNTERCLOCKWISE) # rotate
        under_raster_image_arr = cv2.flip(under_raster_image_arr, 0) # flip

        # set the maximum value to 255
        normarize_constant = np.max(under_raster_image_arr)
        under_raster_image_arr = (under_raster_image_arr/normarize_constant * 255).astype(np.uint8)
        
        
        # convert RGB to BGR
        under_raster_image_arr = under_raster_image_arr[:, :, ::-1]

        # overlap road map on Landsat8 image 
        height, width, _ = under_raster_image_arr.shape
        road_arr = np.zeros((height, width, 3), np.uint8)
        road_arr[:] = (255, 0, 0)

        overlaped_image = np.where(over_image_arr==(0,0,0),
                                   under_raster_image_arr,
                                   over_image_arr)
        
        return overlaped_image

    @classmethod
    def histogram_equalization_except_zero(cls, input_image, normarize_constant):
        """
        create histogram equarized image.
        here, black(0) will be ignored.

        input: 
        input_image(ndarray):
            image that will be perfomed histogram equalization.
        
        normarize_constant (float):
            constant to set the maximum pixel value to 255
        
        output:
        histogram_equalization_image(ndarray):
            histgram equalized image (ndarray)
        """
        
        shape = input_image.shape
        histogram_equalization_image = np.zeros(shape)
        input_image = (input_image/normarize_constant * 255).astype(np.uint8)

        non_zero_index = np.where(input_image!=0)

        # calculate histogram equalization and rewrite the result to image
        input_image_non_zero = input_image[non_zero_index]
        histogram_equalization_arr = cv2.equalizeHist(input_image_non_zero)
        histogram_equalization_image[non_zero_index] = np.transpose(histogram_equalization_arr)
        print(histogram_equalization_image.shape)
        
        return histogram_equalization_image

