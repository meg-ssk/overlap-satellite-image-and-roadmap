import toml
import dataclasses

@dataclasses.dataclass
class SettingsData:
    """
    class variable for pre-defined parameters
    """
    scene_url : str
    image_download_directory : str
    output_image_directory : str
    EPSG : int
    crop_area : list

class SettingsDataLoader:
    def __init__(self, path_to_toml_file):
        """
        input:
        path_to_toml_file (str):
            path to "settings.toml" that describes parameters.

        """
        self.path_to_toml_file = path_to_toml_file

    def load_toml_file(self):
        """
        output (dataclass):
            dataclass incliding parameters loaded from "settings.toml".
        """

        with open(self.path_to_toml_file) as file:
            data = toml.load(self.path_to_toml_file)
        return SettingsData(**data)