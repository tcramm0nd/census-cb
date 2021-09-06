# census-cb
[![PyPI](https://img.shields.io/pypi/v/census-cb)](https://pypi.org/project/census-cb/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/census-cb)](https://pypi.org/project/census-cb/)
[![GitHub License](https://img.shields.io/github/license/tcramm0nd/census-cb)](https://github.com/tcramm0nd/census-cb/blob/main/LICENSE)

`census-cb` is a wrapper for downloading and processing Cartography Boundaries from the US Census Bureau. It stands for Census Cartographic Boundaries; apparently that's confusing (but, like most things, it made sense at the time).

The goal of `census-cb` is to provide an easy way to get GIS information created by the United States Census Bureau. There's a wide variety of cartographic files availbable for download, such as state and county lines, voting district, Tribal subdivisions, and more!
### Entiry Information
There are a designated set of entities available for download from the census bureau. Each year of available data has a specific set of available entities, and the shape of these entities may change from year to year. You can find a full list [pdf of available entities for download](https://www2.census.gov/geo/tiger/GENZ2020/2020_file_name_def.pdf) on the US Census Bureau site.
## Installation
Install using `pip`
```(python)
pip install census-cb
```

## Usage

```(python)
# Create a Boundary File for the desired entity
bf = BoundaryFile(2020, 'us', 'state', '500k')

# Create a processor for downloading and unpacking the data
pcbf = ProcessCBF(bf, 'gdf')

# Get the Data
pcbf.get()
```

## Examples
Download and display the state boudnaries from the US Census Bureau.
```(python)
# Create a Boundary File for the US State Lines
state_boundary_file = BoundaryFile(2020, 'us', 'state', '500k')

# Create a processor that returns a GeoDataFrame
pcbf = ProcessCBF(state_boundary_file, 'gdf')

# Get the Data
state_lines = pcbf.get()

# See the Data
state_lines.plot()
```

## To Do
- provide some better functionality for editing Entity Information after a BoundaryFile object is declared
- update `__str__` to return the attributes of the boudnary file
- instantiate ProcessCBF as empty, so multiple boundary files can be passed to it.
- build out factory setting for Processor. Also, change the name!






