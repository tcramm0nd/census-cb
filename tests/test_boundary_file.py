import pytest
from census_cb.census_cb import BoundaryFile
from requests.models import HTTPError


@pytest.fixture
def example_bf():
    bf = BoundaryFile(2020, 'us', 'state', '500k')
    return bf

def test_bf_years(caplog):
    BoundaryFile(2009, 'us', 'state', '500k')
    assert 'Files before the year 2010 are not supported!' in caplog.text
    
def test_bf_file_type():
    with pytest.raises(TypeError) as e:
        BoundaryFile(2020, 'us', 'state', '500k', file_type='xyz')
        
def test_bf_default_filetype(example_bf):
    assert example_bf.file_type == 'shp'
    
def test_bf_url(example_bf):
    assert example_bf.url == 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_500k.zip'
    
def test_url_validator_fail():
    bf = BoundaryFile(2020, 'us', 'state', '5000k')
    with pytest.raises(HTTPError) as e:
        bf.validate_url()

def test_url_validator(example_bf, caplog):
    example_bf.validate_url()
    assert 'No issues found. Great!' in caplog.text
