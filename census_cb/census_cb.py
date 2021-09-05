import io
import logging
import os
import zipfile
from urllib.parse import urljoin

import requests

# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BoundaryFile():
    BASE = "https://www2.census.gov/geo/tiger/"
    def __init__(self, year, state, entity, resolution, file_type='shp'):
        if year >= 2010:
            self.year_folder = f'GENZ{year}'
        else:
            self.year_folder = f'TIGER{year}'
            logger.warning('Files before the year 2010 are not supported!')
                
        if file_type not in ['shp', 'kml', 'gbd']:
            raise TypeError
        else:
            self.file_type = file_type
        
        
        self.file_name = f'cb_{year}_{state}_{entity}_{resolution}.zip'
        self.url = self._generate_url()
        
    def _generate_url(self):
        url_path = '/'.join([self.year_folder, self.file_type, self.file_name])
        return urljoin(self.BASE, url_path)
    def validate_url(self):
        year_url = urljoin(self.BASE, self.year_folder)
        self._validator(year_url)
        file_url = urljoin(self.BASE, '/'.join([self.year_folder, self.file_type]))
        self._validator(file_url)
        self._validator(self.url)
        logger.info('No issues found. Great!')
    def _validator(self, url):
        response = requests.head(url)
        response.raise_for_status()

class ProcessCBF():
    # https://gis.stackexchange.com/questions/225586/reading-raw-data-into-geopandas
    def __init__(self, boundary_file, format, path=None) -> None:
        """Fetches and processes a boundary file based on the desired return format.
        Currently supported formates are File and GeoDataFrames.

        Args:
            boundary_file (BoundaryFile): a BoundaryFile object
            format (str): method for returning or storing the data
        """        
        self.cbf_url = boundary_file.url
        self.format = format
        self.filename = boundary_file.file_name
        self.folder = self._set_folder(path)
        
    def _set_folder(self, path):
        if self.format == 'gdf' and not path:
            path = '/tmp'
        if path:
            return os.path.join(path, self.filename[:-4])
        else:
            return self.filename[:-4]
            
    def _get(self):
        try:
            response = requests.get(self.cbf_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response.content
    
    def _extract_data(self):
        data = self._get()
        z = zipfile.ZipFile(io.BytesIO(data))
        z.extractall(self.folder)
    def get(self):
        if self.format == 'file':
            self._extract_data()
            logger.info(f'Successfully downloaded {self.filename} to {self.folder}')
        elif self.format == 'gdf':
            import geopandas as gpd
            return gpd.GeoDataFrame(self._extract_data)
