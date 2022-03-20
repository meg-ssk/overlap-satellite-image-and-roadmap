import sys
sys.path.append('./')
from src.lib.loader.settings_loader import SettingsData, SettingsDataLoader
import pytest


@pytest.mark.parametrize(('parameter', 'expected'), [
    ('scene_url', "https://s3-us-west-2.amazonaws.com/landsat-pds/c1/L8/044/034/LC08_L1TP_044034_20190706_20190706_01_RT/index.html"),
    ('image_download_directory', "./materials/images/"),
    ('output_image_directory', "./output-images/"),
    ('EPSG', 32610),
    ('crop_area', [542645, 4184720, 554019, 4176372])
])


def test_load_toml_file(parameter, expected):
    res = SettingsDataLoader('./settings.toml').load_toml_file()
    assert res.__dict__[parameter] == expected
