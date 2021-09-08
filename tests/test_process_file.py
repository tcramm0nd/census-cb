import pytest
from src.census_cb.census_cb import BoundaryFile, CBFProcessor
from geopandas import GeoDataFrame

@pytest.fixture
def example_bf():
    return BoundaryFile(2020, 'us', 'state', '500k')

@pytest.fixture
def example_cbfp(example_bf):
    return CBFProcessor('file', example_bf)

@pytest.mark.parametrize('data_format, expected_path',
                         [(['gdf', None], 'cb_2020_us_state_500k'),
                          (['gdf', '~/Downloads'], '~/Downloads/cb_2020_us_state_500k'),
                          (['file', None], 'cb_2020_us_state_500k'),
                          (['file', '/Downloads'], '/Downloads/cb_2020_us_state_500k')])
def test_folder(data_format, expected_path, example_bf):
    cbfp = CBFProcessor(data_format[0], example_bf, path=data_format[1])
    assert cbfp.folder == expected_path

def test_data_format():
    with pytest.raises(ValueError):
        CBFProcessor('xyz')

def test_get(example_cbfp):
    assert len(example_cbfp._get()) == 3413716

def test_get_fail():
    with pytest.raises(SystemExit):
        CBFProcessor('file', BoundaryFile(2020, 'us', 'sate', '5000k'))._get()

def test_gdf_generation(example_bf):
    cbfp = CBFProcessor('gdf', example_bf, path='~/Downloads')
    gdf = cbfp.process_data()
    assert type(gdf) == type(GeoDataFrame())

# def test_file_extraction(example_cbfp):
#     example_cbfp.get()