import requests

class ImageDataDownloader:
    @classmethod    
    def image_data_downloader(cls, settings):
        """
        download landsat8 images of bands 2-4 (2: red, 3: green, 4: blue).

        input: 
        settings (dataclass)
            pre-defined parameters, we need directory where landsat images will be saved.
        output:
            we can download 3 landsat images
        """
        # read scene url from AWS
        scene_url = settings.scene_url
        scene_id = scene_url.split('/')[-2]
        
        # set url to each RGB band images
        image_url_blue = scene_url[:-10] + scene_id + "_B2.TIF"
        image_url_green = scene_url[:-10] + scene_id + "_B3.TIF"
        image_url_red = scene_url[:-10] + scene_id + "_B4.TIF"

        image_url_list = [image_url_red, image_url_green, image_url_blue]
        colors_list = ["red", "green", "blue"]

        # download 3 bands landsat8 images
        print("downloading landsat8 image...")
        for i in range(len(image_url_list)):
            print("downloading " + colors_list[i] + " image...")
            image_url = image_url_list[i]
            url_data = requests.get(image_url).content
            file_name = settings.image_download_directory + colors_list[i] + ".tiff"
            with open(file_name, mode='wb') as f:
                f.write(url_data)
        
        return 


