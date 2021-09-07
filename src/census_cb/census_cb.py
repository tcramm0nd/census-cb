import io
import logging
import os
import zipfile
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BoundaryFile():
    BASE = "https://www2.census.gov/geo/tiger/"
    def __init__(self, year, state, entity, resolution, file_type='shp'):
        """Creates a Boundary File URL object validated against the available entries per year

        Args:
            year (int): Year of the Census Cartographic Boundary File.
            state (str): The state fips code or 'us' for a national level file.
            entity (str): The name of the entity to be retrieved.
            resolution (str): Resolution of the file; 500k, 5m, or 20m.
            file_type (str, optional): [description]. Defaults to 'shp'. KML and GDB are also available.
        """
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
        """Wrapper function to create a url for Cartographic Boundary retireval.

        Returns:
            str: A URL string for the boundary file
        """
        url_path = '/'.join([self.year_folder, self.file_type, self.file_name])
        return urljoin(self.BASE, url_path)
    
    def validate_url(self):
        """Validates the generated URL."""
        year_url = urljoin(self.BASE, self.year_folder)
        self._validator(year_url)
        file_url = urljoin(self.BASE, '/'.join([self.year_folder, self.file_type]))
        self._validator(file_url)
        self._validator(self.url)
        logger.info('No issues found. Great!')
        
    def _validator(self, url):
        """Wraps the raise_for_status() call from requests.

        Args:
            url (str): URL to be validated
        """
        response = requests.head(url)
        response.raise_for_status()

class ProcessCBF():
    def __init__(self, boundary_file, data_format, path=None):
        """Fetches and processes a boundary file based on the desired return format.Currently supported formates are File and GeoDataFrames.

        Args:
            boundary_file (BoundaryFile): BoundaryFile object
            format (str): Format option of either file or GeoDataFrame
            path (str, optional): Path to save the extracted data. Defaults to None.
        """            
        self.cbf_url = boundary_file.url
        self.data_format = data_format
        self.filename = f'{boundary_file.file_name[:-4]}.{boundary_file.file_type}'
        self.folder = self._set_folder(path)
        
    def _set_folder(self, path):
        """Sets the destination folder for the downloaded data

        Args:
            path (str): The desired path to save the extraction folder

        Returns:
            str: the folder joined with the path
        """        
        if path:
            return os.path.join(path, self.filename[:-4])
        else:
            return self.filename[:-4]
            
    def _get(self):
        """Returns bytes-level content of the Cartographic Boundary Zipfile

        Raises:
            SystemExit: Exits when an incorrect URL is called

        Returns:
             eytes: Byte-response content
        """        
        try:
            response = requests.get(self.cbf_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response.content
    
    def _extract_data_to_file(self, data):
        """Extracts data to be saved locally

        Args:
            data (bytes): Bytes data from the BoundaryFile
        """        
        z = zipfile.ZipFile(io.BytesIO(data))
        z.extractall(self.folder)

    def _extract_data_to_gdf(self, data):
        """Instantiates a GeoDataFrame.

        Args:
            data (bytes): Bytes data from the BoundaryFile

        Returns:
            GeoDataFrame: Returns a GeoDataFrame
        """        
        from fiona.io import ZipMemoryFile
        import geopandas as gpd
        
        zipshp = io.BytesIO(data)
        with (ZipMemoryFile(zipshp)) as file:
            with file.open() as gdf_source:
                crs = gdf_source.crs
                gdf = gpd.GeoDataFrame.from_features(gdf_source, crs=crs)
                
        return gdf        
    
    def get(self):
        """Gets a Census Bureau Cartographic Boundary File."""
        data = self._get()
        if self.data_format == 'gdf':
            return self._extract_data_to_gdf(data)
        elif self.data_format == 'file':
            self._extract_data_to_file(data)