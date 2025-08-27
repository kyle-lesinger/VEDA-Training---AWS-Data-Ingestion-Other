# Cloud Optimized GeoTIFF (COG) Conversions Guide

## Table of Contents
- [What are Cloud Optimized GeoTIFFs?](#what-are-cloud-optimized-geotiffs)
- [Why COGs are Important](#why-cogs-are-important)
- [Installing GDAL on macOS](#installing-gdal-on-macos)
- [Common COG Conversion Operations](#common-cog-conversion-operations)
- [Python GDAL Usage](#python-gdal-usage)
- [VEDA Platform Integration](#veda-platform-integration)
- [Best Practices](#best-practices)
- [Helpful Resources](#helpful-resources)

## What are Cloud Optimized GeoTIFFs?

Cloud Optimized GeoTIFFs (COGs) are regular GeoTIFF files with an internal organization that enables more efficient workflows in cloud environments. The key difference is that COGs are structured to support **HTTP range requests**, allowing clients to request only the portions of data they need without downloading the entire file.

### Key Features:
- **Tiled internal structure**: Data is organized in tiles (typically 256x256 or 512x512 pixels)
- **Overviews (pyramids)**: Pre-computed lower resolution versions for faster visualization at different zoom levels
- **HTTP GET range request support**: Enables partial reads over the network
- **Compression**: Supports various compression algorithms (LZW, DEFLATE, ZSTD)
- **Standard GeoTIFF format**: Compatible with existing GeoTIFF readers

### Technical Specifications:
- Internal tiling (typically 512x512 pixels)
- Compressed using DEFLATE, LZW, or other algorithms
- Contains internal overviews/pyramids
- Organized with the header and overview IFDs at the beginning of the file

## Why COGs are Important

### 1. **Cloud-Native Architecture**
- Designed for cloud object storage (S3, Azure Blob, Google Cloud Storage)
- No need for specialized tile servers or databases
- Direct access from web applications

### 2. **Performance Benefits**
- **Partial reads**: Only download the data you need
- **Faster visualization**: Pre-computed overviews enable quick rendering at any zoom level
- **Reduced bandwidth**: Minimize data transfer costs
- **Parallel processing**: Multiple tiles can be read simultaneously

### 3. **Cost Efficiency**
- Lower storage costs compared to traditional tile pyramids
- Reduced compute requirements (no tile server needed)
- Minimal data egress charges

### 4. **Interoperability**
- Works with standard GeoTIFF readers
- Compatible with modern geospatial tools (QGIS, ArcGIS, GDAL)
- Supports STAC (SpatioTemporal Asset Catalog) specifications

## Installing GDAL on macOS

### Method 1: Using Homebrew (Recommended)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install GDAL
brew install gdal

# Verify installation
gdal-config --version
gdalinfo --version
```

### Method 2: Using Conda/Mamba
```bash
# Using conda
conda install -c conda-forge gdal

# Using mamba (faster)
mamba install -c conda-forge gdal

# Verify installation
gdalinfo --version
```

### Method 3: Using MacPorts
```bash
# Install MacPorts from https://www.macports.org/install.php

# Install GDAL
sudo port install gdal +complete +python39

# Verify installation
gdalinfo --version
```

### Installing Python GDAL Bindings
```bash
# Using pip (ensure GDAL is installed first)
pip install GDAL==$(gdal-config --version)

# Or using conda/mamba
conda install -c conda-forge gdal python-gdal
```

## Common COG Conversion Operations

### Basic COG Creation
```bash
# Simple COG creation with defaults
gdal_translate input.tif output_cog.tif -of COG

# With compression and tiling options
gdal_translate input.tif output_cog.tif \
  -of COG \
  -co COMPRESS=DEFLATE \
  -co TILING_SCHEME=GoogleMapsCompatible
```

### Advanced COG Creation with Overviews
```bash
# Create COG with specific tile size and compression
gdal_translate input.tif output_cog.tif \
  -of COG \
  -co TILING_SCHEME=GoogleMapsCompatible \
  -co COMPRESS=LZW \
  -co BLOCKSIZE=512 \
  -co OVERVIEWS=IGNORE_EXISTING \
  -co BIGTIFF=YES
```

### Validate COG Structure
```bash
# Check if a file is a valid COG
rio cogeo validate output_cog.tif

# Or using GDAL's validate_cloud_optimized_geotiff.py
python validate_cloud_optimized_geotiff.py output_cog.tif
```

### Batch Conversion
```bash
# Convert all TIFFs in a directory to COGs
for file in *.tif; do
    gdal_translate "$file" "cog_${file}" \
      -of COG \
      -co COMPRESS=DEFLATE \
      -co PREDICTOR=2
done
```

### NetCDF to COG Conversion
```bash
# Extract a band from NetCDF and convert to COG
gdal_translate NETCDF:"input.nc":variable_name output_cog.tif \
  -of COG \
  -co COMPRESS=DEFLATE \
  -co RESAMPLING=AVERAGE
```

### Reprojection and COG Creation
```bash
# Reproject to Web Mercator and create COG
gdalwarp -t_srs EPSG:3857 input.tif temp.tif
gdal_translate temp.tif output_cog.tif -of COG
rm temp.tif

# Or in one step using VRT
gdalwarp -t_srs EPSG:3857 input.tif output_cog.tif -of COG
```

## Python GDAL Usage

Most GDAL command-line operations can be performed in Python using the GDAL Python bindings or higher-level libraries like Rasterio.

### Using GDAL Python Bindings
```python
from osgeo import gdal

# Open source file
src_ds = gdal.Open('input.tif')

# Create COG with gdal.Translate
gdal.Translate(
    'output_cog.tif',
    src_ds,
    format='COG',
    creationOptions=['COMPRESS=DEFLATE', 'TILING_SCHEME=GoogleMapsCompatible']
)

# Close dataset
src_ds = None
```

### Using Rasterio (More Pythonic)
```python
import rasterio
from rasterio.enums import Resampling

# Read source file
with rasterio.open('input.tif') as src:
    profile = src.profile.copy()
    
    # Update profile for COG
    profile.update({
        'driver': 'COG',
        'compress': 'deflate',
        'blockxsize': 512,
        'blockysize': 512,
        'tiled': True,
        'interleave': 'pixel'
    })
    
    # Write COG
    with rasterio.open('output_cog.tif', 'w', **profile) as dst:
        for i in range(1, src.count + 1):
            dst.write(src.read(i), i)
        
        # Build overviews
        dst.build_overviews([2, 4, 8, 16], Resampling.average)
```

### Using Rio-cogeo Library
```python
from rio_cogeo.cog import cog_translate
from rio_cogeo.profiles import cog_profiles

# Simple COG creation
cog_translate(
    'input.tif',
    'output_cog.tif',
    cog_profiles.get("deflate"),
)

# With custom options
cog_translate(
    'input.tif',
    'output_cog.tif',
    cog_profiles.get("lzw"),
    overview_level=5,
    overview_resampling="average",
    web_optimized=True
)
```

### Batch Processing in Python
```python
import os
from pathlib import Path
from rio_cogeo.cog import cog_translate
from rio_cogeo.profiles import cog_profiles

# Convert all TIFFs in a directory
input_dir = Path('./input_data')
output_dir = Path('./cog_output')
output_dir.mkdir(exist_ok=True)

for tif_file in input_dir.glob('*.tif'):
    output_file = output_dir / f'cog_{tif_file.name}'
    
    cog_translate(
        str(tif_file),
        str(output_file),
        cog_profiles.get("deflate"),
        quiet=False
    )
    
    print(f"Converted {tif_file.name} to COG")
```

## VEDA Platform Integration

The [VEDA (Visualization, Exploration, and Data Analysis) platform](https://docs.openveda.cloud/) requires properly formatted Cloud Optimized GeoTIFFs for optimal performance.

### VEDA COG Requirements

1. **STAC Compliance**: COGs should be cataloged with STAC metadata
2. **Projection**: Web Mercator (EPSG:3857) or Geographic (EPSG:4326) preferred
3. **Tiling Scheme**: GoogleMapsCompatible recommended for web visualization
4. **Compression**: DEFLATE or LZW with predictor
5. **Overviews**: Required for multi-scale visualization

### VEDA-Specific Resources

- **[VEDA Documentation](https://docs.openveda.cloud/)**: Complete platform documentation
- **[Data Ingestion Guide](https://docs.openveda.cloud/contributing/dataset-ingestion/)**: Step-by-step ingestion process
- **[VEDA Notebooks](https://docs.openveda.cloud/exploration-and-analysis/exploration-and-analysis/)**: 
  - "Open and plot COGs"
  - "Calculate timeseries from COGs"
  - "Converting NetCDF to COG (CMIP6)"

### Example: Preparing Data for VEDA
```python
import rasterio
from rio_cogeo.cog import cog_translate
from rio_cogeo.profiles import cog_profiles
import json

def prepare_cog_for_veda(input_file, output_file):
    """
    Prepare a COG optimized for VEDA platform ingestion
    """
    # Define COG profile optimized for cloud delivery
    profile = cog_profiles.get("deflate")
    profile.update({
        'blocksize': 512,
        'overview_resampling': 'average'
    })
    
    # Create COG
    cog_translate(
        input_file,
        output_file,
        profile,
        web_optimized=True,
        overview_level=5
    )
    
    # Generate STAC item metadata
    with rasterio.open(output_file) as src:
        bounds = src.bounds
        stac_item = {
            "type": "Feature",
            "stac_version": "1.0.0",
            "id": Path(output_file).stem,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [bounds.left, bounds.bottom],
                    [bounds.right, bounds.bottom],
                    [bounds.right, bounds.top],
                    [bounds.left, bounds.top],
                    [bounds.left, bounds.bottom]
                ]]
            },
            "bbox": [bounds.left, bounds.bottom, bounds.right, bounds.top],
            "properties": {
                "datetime": datetime.now().isoformat()
            },
            "assets": {
                "cog": {
                    "href": output_file,
                    "type": "image/tiff; application=geotiff; profile=cloud-optimized"
                }
            }
        }
    
    return stac_item
```

## Best Practices

### 1. **Compression Settings**
- Use **DEFLATE** for general purpose (good compression, wide compatibility)
- Use **LZW** with PREDICTOR=2 for continuous data (elevation, temperature)
- Use **JPEG** for RGB imagery (lossy but efficient)
- Use **ZSTD** for best compression ratio (requires GDAL 2.3+)

### 2. **Tile Size**
- **512x512**: Good balance for most use cases
- **256x256**: Better for many small requests
- **1024x1024**: Better for large area processing

### 3. **Overview Levels**
```bash
# Calculate appropriate overview levels
gdaladdo -r average input.tif 2 4 8 16 32 64
```

### 4. **Validation**
Always validate COGs after creation:
```bash
# Using rio-cogeo
rio cogeo validate output_cog.tif

# Using GDAL script
python validate_cloud_optimized_geotiff.py output_cog.tif
```

### 5. **NoData Handling**
```bash
# Set NoData value during COG creation
gdal_translate input.tif output_cog.tif \
  -of COG \
  -a_nodata -9999 \
  -co COMPRESS=DEFLATE
```

### 6. **Color Interpretation**
```bash
# Preserve color interpretation for RGB images
gdal_translate input.tif output_cog.tif \
  -of COG \
  -co COMPRESS=JPEG \
  -co PHOTOMETRIC=YCBCR
```

## Helpful Resources

### Official Documentation
- **[COG Specification](https://www.cogeo.org/)**: Official Cloud Optimized GeoTIFF website
- **[GDAL COG Driver](https://gdal.org/drivers/raster/cog.html)**: GDAL's COG driver documentation
- **[OGC COG Standard](https://docs.ogc.org/is/21-026/21-026.html)**: Official OGC standard

### Tools and Libraries
- **[Rio-cogeo](https://github.com/cogeotiff/rio-cogeo)**: Python library for COG creation
- **[GDAL](https://gdal.org/)**: Geospatial Data Abstraction Library
- **[Rasterio](https://rasterio.readthedocs.io/)**: Python library for raster data
- **[COG Validator](https://github.com/OSGeo/gdal/blob/master/swig/python/gdal-utils/osgeo_utils/samples/validate_cloud_optimized_geotiff.py)**: Python script to validate COGs

### Tutorials and Guides
- **[COG Tutorial by Planet](https://developers.planet.com/docs/planetschool/cloud-optimized-geotiffs-cogs/)**: Comprehensive COG tutorial
- **[MapBox COG Guide](https://docs.mapbox.com/help/troubleshooting/cog-guide/)**: Practical COG usage guide
- **[STAC Best Practices](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)**: STAC catalog best practices

### VEDA-Specific Resources
- **[VEDA Platform](https://www.earthdata.nasa.gov/esds/veda)**: NASA's VEDA platform overview
- **[VEDA Documentation](https://docs.openveda.cloud/)**: Complete documentation
- **[VEDA GitHub](https://github.com/NASA-IMPACT/veda-docs)**: VEDA documentation repository
- **[VEDA Jupyter Notebooks](https://docs.openveda.cloud/exploration-and-analysis/exploration-and-analysis/)**: Interactive examples

### Community Resources
- **[COG Talk Discourse](https://www.cogeo.org/talk/)**: Community forum
- **[Awesome COG](https://github.com/cholmes/awesome-cog)**: Curated list of COG resources
- **[GDAL Mailing List](https://lists.osgeo.org/mailman/listinfo/gdal-dev)**: GDAL developer discussions

## Quick Reference

### Check if file is COG
```bash
rio cogeo validate file.tif
```

### Create basic COG
```bash
gdal_translate input.tif output.tif -of COG
```

### Create optimized COG for web
```bash
gdal_translate input.tif output.tif \
  -of COG \
  -co TILING_SCHEME=GoogleMapsCompatible \
  -co COMPRESS=DEFLATE
```

### Python one-liner
```python
from rio_cogeo.cog import cog_translate
cog_translate("input.tif", "output.tif", web_optimized=True)
```

---

*Last updated: 2025*