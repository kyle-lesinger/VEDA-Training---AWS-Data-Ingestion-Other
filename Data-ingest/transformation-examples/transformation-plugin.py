"""
Transformation Plugin for ECCO Darwin CO2 Flux Dataset
This plugin demonstrates how to create a reusable transformation function
for automated data ingestion pipelines.
"""

import re
from typing import Dict
import xarray
from s3fs import S3File
from xarray import DataArray


def ecco_darwin_transformation(
    file_obj: S3File, name: str, nodata: int
) -> Dict[str, DataArray]:
    """
    Transformation function for the ECCO Darwin dataset
    
    This function transforms NetCDF data from the ECCO Darwin model
    into Cloud Optimized GeoTIFFs (COGs) suitable for ingestion into
    the GHG Center STAC catalog.
    
    Args:
        file_obj (s3fs object): S3 file object for one file of the dataset
        name (str): Name of the file to be transformed
        nodata (int): NoData value as specified by the data provider
    
    Returns:
        dict: Dictionary with COG filename as key and data array as value
              Each entry will be written as a separate COG file
    
    Example:
        >>> from s3fs import S3FileSystem
        >>> fs = S3FileSystem()
        >>> file_obj = fs.open('s3://bucket/path/to/file.nc')
        >>> result = ecco_darwin_transformation(file_obj, 'file.nc', -9999)
        >>> for cog_name, data in result.items():
        ...     data.rio.to_raster(f"output/{cog_name}")
    """
    var_data_netcdf = {}
    
    # Open the NetCDF dataset
    xds = xarray.open_dataset(file_obj)
    
    # Rename dimensions to standard names
    xds = xds.rename({"y": "latitude", "x": "longitude"})
    
    # Transform coordinates from grid indices to lat/lon
    # Original data uses grid indices (0-1440 for lon, 0-721 for lat)
    # Convert to standard geographic coordinates
    xds = xds.assign_coords(
        longitude=((xds.longitude / 1440) * 360) - 180
    ).sortby("longitude")
    
    xds = xds.assign_coords(
        latitude=((xds.latitude / 721) * 180) - 90
    ).sortby("latitude")
    
    # Get list of data variables (skip first 2 which are usually dimension vars)
    variables = list(xds.data_vars)[2:]
    
    # Process each variable
    for var in variables:
        # Extract filename components for creating output name
        filename = name.split("/")[-1]
        filename_elements = re.split("[_ .]", filename)
        
        # Get the data array for this variable
        data = xds[var]
        
        # Reindex latitude to ensure correct orientation
        data = data.reindex(latitude=list(reversed(data.latitude)))
        
        # Replace nodata values with -9999 (standard for COGs)
        data = data.where(data != nodata, -9999)
        
        # Set spatial dimensions and CRS for rasterio
        data.rio.set_spatial_dims("longitude", "latitude", inplace=True)
        data.rio.write_crs("epsg:4326", inplace=True)
        data.rio.write_nodata(-9999, inplace=True)
        
        # Create output filename
        # Remove extension
        filename_elements.pop()
        # Combine date elements
        filename_elements[-1] = filename_elements[-2] + filename_elements[-1]
        filename_elements.pop(-2)
        # Create final filename
        cog_filename = "_".join(filename_elements)
        cog_filename = f"{cog_filename}.tif"
        
        # Add to output dictionary
        var_data_netcdf[cog_filename] = data
    
    return var_data_netcdf


def create_transformation_plugin(dataset_config: dict):
    """
    Factory function to create dataset-specific transformation plugins
    
    Args:
        dataset_config (dict): Configuration dictionary containing:
            - coordinate_mapping: How to map coordinates
            - variable_selection: Which variables to process
            - filename_pattern: How to construct output filenames
            - nodata_handling: How to handle NoData values
    
    Returns:
        function: Transformation function for the specified dataset
    
    Example configuration:
    {
        "coordinate_mapping": {
            "x": "longitude",
            "y": "latitude"
        },
        "variable_selection": {
            "skip_first": 2,
            "include": ["co2_flux", "ch4_flux"],
            "exclude": ["time_bounds"]
        },
        "filename_pattern": "{collection}_{variable}_{date}.tif",
        "nodata_handling": {
            "input": -999999,
            "output": -9999
        }
    }
    """
    def transform(file_obj, name, nodata):
        # Implementation would use dataset_config to customize transformation
        # This is a template for creating flexible transformation functions
        pass
    
    return transform


# Additional utility functions for common transformation tasks

def fix_longitude_wrap(data: xarray.Dataset) -> xarray.Dataset:
    """
    Fix longitude coordinates from 0-360 to -180-180 convention
    
    Args:
        data: xarray Dataset with longitude coordinates
    
    Returns:
        Dataset with corrected longitude coordinates
    """
    if "longitude" in data.dims:
        data = data.assign_coords(
            longitude=(((data.longitude + 180) % 360) - 180)
        ).sortby("longitude")
    elif "lon" in data.dims:
        data = data.assign_coords(
            lon=(((data.lon + 180) % 360) - 180)
        ).sortby("lon")
    
    return data


def apply_scale_and_offset(
    data: DataArray,
    scale_factor: float = 1.0,
    add_offset: float = 0.0
) -> DataArray:
    """
    Apply scale factor and offset to data values
    
    Args:
        data: Input data array
        scale_factor: Multiplicative scale factor
        add_offset: Additive offset
    
    Returns:
        Scaled and offset data array
    """
    return data * scale_factor + add_offset


def create_cog_profile(data_type: str) -> dict:
    """
    Create appropriate COG profile based on data type
    
    Args:
        data_type: numpy dtype string (e.g., 'float32', 'int16')
    
    Returns:
        Dictionary with COG creation parameters
    """
    base_profile = {
        "driver": "COG",
        "compress": "DEFLATE",
        "TILED": True,
        "BLOCKXSIZE": 512,
        "BLOCKYSIZE": 512
    }
    
    # Special handling for float data types
    if data_type in ['float32', 'float64']:
        base_profile.update({
            "PREDICTOR": 1,  # No predictor for float data
            "ZLEVEL": 6,
            "BIGTIFF": "YES"
        })
    elif data_type in ['int16', 'int32']:
        base_profile.update({
            "PREDICTOR": 2,  # Horizontal differencing for integers
            "ZLEVEL": 6
        })
    
    return base_profile


def validate_transformation_output(data: DataArray) -> bool:
    """
    Validate that transformed data meets requirements
    
    Args:
        data: Transformed data array
    
    Returns:
        True if data is valid, False otherwise
    """
    # Check for required attributes
    if not hasattr(data, 'rio'):
        return False
    
    # Check for CRS
    if data.rio.crs is None:
        return False
    
    # Check for valid dimensions
    if len(data.dims) < 2:
        return False
    
    # Check for NoData value
    if data.rio.nodata is None:
        return False
    
    return True


# Example usage in a DAG or pipeline
if __name__ == "__main__":
    # Example configuration
    example_config = {
        "collection": "ecco-darwin-co2flux",
        "source_bucket": "ghgc-data-raw",
        "source_prefix": "ecco_darwin/",
        "target_bucket": "ghgc-data-store-develop",
        "target_prefix": "transformed_cogs/ecco-darwin/",
        "nodata_value": -999999
    }
    
    print("Transformation plugin loaded successfully")
    print(f"Configuration: {example_config}")
    print("\nThis plugin can be imported and used in data transformation pipelines")
    print("Example: from transformation_plugin import ecco_darwin_transformation")