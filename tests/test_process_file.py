import pytest
from census_cb.census_cb import BoundaryFile, ProcessCBF
from geopandas import GeoDataFrame

@pytest.fixture
def example_bf():
    return BoundaryFile(2020, 'us', 'state', '500k')

@pytest.fixture
def example_pcbf(example_bf):
    return ProcessCBF(example_bf, 'file')

@pytest.mark.parametrize('data_format, expected_path', 
                         [(['gdf', None], 'cb_2020_us_state_500k'),
                          (['gdf', '~/Downloads'], '~/Downloads/cb_2020_us_state_500k'),
                          (['file', None], 'cb_2020_us_state_500k'),
                          (['file', '/Downloads'], '/Downloads/cb_2020_us_state_500k')])
def test_folder(data_format, expected_path, example_bf):
    pcbf = ProcessCBF(example_bf, data_format[0], path=data_format[1])
    assert pcbf.folder == expected_path

def test_get(example_pcbf):
    assert len(example_pcbf._get()) == 3413716
    
def test_get_fail():
    with pytest.raises(SystemExit) as e:
        ProcessCBF(BoundaryFile(2020, 'us', 'sate', '5000k'), 'file')._get()

def test_gdf_generation(example_bf):
    pcbf = ProcessCBF(example_bf, 'gdf', path='~/Downloads')
    gdf = pcbf.get()
    assert type(gdf) == type(GeoDataFrame())

# def test_file_extraction(example_pcbf):
#     example_pcbf.get()