# STAC (SpatioTemporal Asset Catalog) Training Guide

## Table of Contents
1. [Introduction to STAC](#introduction-to-stac)
2. [Why STAC Matters](#why-stac-matters)
3. [Core STAC Concepts](#core-stac-concepts)
4. [STAC Specification Components](#stac-specification-components)
5. [Unique Features of STAC](#unique-features-of-stac)
6. [STAC in the VEDA Platform](#stac-in-the-veda-platform)
7. [Working with STAC APIs](#working-with-stac-apis)
8. [Python Libraries for STAC](#python-libraries-for-stac)
9. [Practical Examples](#practical-examples)
10. [STAC Best Practices](#stac-best-practices)
11. [Resources and Links](#resources-and-links)

---

## Introduction to STAC

### What is STAC?

**STAC (SpatioTemporal Asset Catalog)** is an open-source specification that provides a common language to describe geospatial information, making it easier to index and discover data across multiple platforms and organizations.

Think of STAC as the **"HTML of geospatial data"** – it provides a standardized way to:
- 📍 Describe the **location** of data
- ⏰ Specify the **time** when data was collected
- 📊 List available **assets** (files, bands, metadata)
- 🔍 Enable **searchable** catalogs of Earth observation data

### The Problem STAC Solves

Before STAC, organizations faced significant challenges:

```
Traditional Approach:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ NASA Format  │  │ ESA Format   │  │ USGS Format  │
│   Custom     │  │   Different  │  │   Unique     │
│   APIs       │  │   Structure  │  │   Metadata   │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                ↓                ↓
    [Complex Integration Required for Each Source]

With STAC:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ NASA STAC    │  │ ESA STAC     │  │ USGS STAC    │
│ Standard API │  │ Standard API │  │ Standard API │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                ↓                ↓
    [Single Integration Works for All Sources]
```

### Key Benefits

✅ **Interoperability**: Work with data from any provider using the same tools  
✅ **Discoverability**: Search across multiple catalogs with unified queries  
✅ **Efficiency**: Reduce time spent on data wrangling and format conversion  
✅ **Scalability**: Handle massive datasets with cloud-native approaches  
✅ **Community**: Leverage shared tools and libraries  

---

## Why STAC Matters

### For Data Providers

1. **Standardized Publishing**
   - Single format for all data products
   - Reduced documentation burden
   - Easier data sharing

2. **Better Data Management**
   - Organized catalog structure
   - Version control for datasets
   - Clear provenance tracking

3. **Increased Data Usage**
   - More discoverable data
   - Lower barrier to entry
   - Broader user base

### For Data Users

1. **Simplified Discovery**
   ```python
   # Search any STAC catalog with the same syntax
   results = catalog.search(
       bbox=[-180, -90, 180, 90],
       datetime="2024-01-01/2024-01-31",
       query={"eo:cloud_cover": {"lt": 10}}
   )
   ```

2. **Consistent Access Patterns**
   - Same tools work across providers
   - Predictable data structure
   - Reliable metadata

3. **Time and Cost Savings**
   - Less custom code needed
   - Faster prototype development
   - Reduced maintenance

### Real-World Impact

**Example: Disaster Response**
```
Traditional: 3-5 days to integrate multiple data sources
With STAC: 2-4 hours to access and analyze same data
```

**Example: Research Project**
```
Traditional: Custom scripts for each data provider
With STAC: One script handles all providers
```

---

## Core STAC Concepts

### The STAC Hierarchy

```
Catalog
├── Collection 1 (e.g., Landsat-8)
│   ├── Item 1 (Scene from 2024-01-01)
│   │   ├── Asset 1 (Band 1 - Coastal)
│   │   ├── Asset 2 (Band 2 - Blue)
│   │   └── Asset 3 (Thumbnail)
│   └── Item 2 (Scene from 2024-01-02)
│       └── Assets...
└── Collection 2 (e.g., Sentinel-2)
    └── Items...
```

### 1. Catalogs

A **Catalog** is the top-level object that provides an entry point to a STAC dataset.

```json
{
  "stac_version": "1.0.0",
  "type": "Catalog",
  "id": "my-catalog",
  "description": "My Earth Observation Data Catalog",
  "links": [
    {
      "rel": "child",
      "href": "./landsat-8/collection.json",
      "type": "application/json"
    }
  ]
}
```

### 2. Collections

A **Collection** groups related Items that share common properties (e.g., all Landsat-8 scenes).

```json
{
  "stac_version": "1.0.0",
  "type": "Collection",
  "id": "landsat-8",
  "title": "Landsat 8 Collection",
  "description": "Landsat 8 imagery",
  "extent": {
    "spatial": {
      "bbox": [[-180, -90, 180, 90]]
    },
    "temporal": {
      "interval": [["2013-02-11T00:00:00Z", null]]
    }
  },
  "summaries": {
    "eo:bands": [
      {"name": "B1", "common_name": "coastal"},
      {"name": "B2", "common_name": "blue"}
    ]
  }
}
```

### 3. Items

An **Item** represents a single spatiotemporal dataset (e.g., one satellite scene).

```json
{
  "stac_version": "1.0.0",
  "type": "Feature",
  "id": "LC08_L2SP_013031_20240101",
  "collection": "landsat-8",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-122.5, 37.5], [-122.5, 38.5], [-121.5, 38.5], [-121.5, 37.5], [-122.5, 37.5]]]
  },
  "bbox": [-122.5, 37.5, -121.5, 38.5],
  "properties": {
    "datetime": "2024-01-01T18:30:00Z",
    "eo:cloud_cover": 5.2
  },
  "assets": {
    "B1": {
      "href": "https://example.com/data/B1.tif",
      "type": "image/tiff; application=geotiff",
      "title": "Band 1 - Coastal"
    }
  }
}
```

### 4. Assets

**Assets** are the actual files (data, metadata, thumbnails) associated with an Item.

```json
"assets": {
  "data": {
    "href": "s3://bucket/data.tif",
    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
    "roles": ["data"],
    "title": "Cloud Optimized GeoTIFF"
  },
  "thumbnail": {
    "href": "https://example.com/thumb.jpg",
    "type": "image/jpeg",
    "roles": ["thumbnail"],
    "title": "Preview Image"
  },
  "metadata": {
    "href": "https://example.com/metadata.xml",
    "type": "application/xml",
    "roles": ["metadata"]
  }
}
```

---

## STAC Specification Components

### Core Specifications

1. **STAC Item Spec**
   - Defines GeoJSON Feature structure
   - Required fields: id, geometry, bbox, properties, assets
   - Extensible through additional properties

2. **STAC Catalog Spec**
   - Defines catalog structure
   - Links between catalogs, collections, and items
   - Supports static and dynamic catalogs

3. **STAC Collection Spec**
   - Extends Catalog spec
   - Adds extent (spatial and temporal)
   - Includes summaries of Items

4. **STAC API Spec**
   - RESTful API for dynamic catalogs
   - Search endpoints with filtering
   - Based on OGC API - Features

### Common Extensions

STAC is extensible through community-developed extensions:

| Extension | Purpose | Example Use |
|-----------|---------|-------------|
| **eo** | Electro-Optical | Cloud cover, bands |
| **sar** | Synthetic Aperture Radar | Polarization, frequency |
| **projection** | Projection info | CRS, transform |
| **scientific** | Scientific metadata | DOI, citations |
| **raster** | Raster properties | Resolution, data type |
| **pointcloud** | Point cloud data | Density, schema |
| **datacube** | Data cubes | Dimensions, variables |

### STAC API Endpoints

Standard STAC API endpoints:

```
GET  /                        # Landing page
GET  /conformance            # API capabilities
GET  /collections            # List collections
GET  /collections/{id}       # Get collection
GET  /collections/{id}/items # Get items in collection
GET  /search                 # Search items
POST /search                 # Search with body
```

---

## Unique Features of STAC

### 1. Cloud-Native Design

STAC is built for cloud computing:

```python
# Direct cloud access without downloading
import pystac
import rasterio

# Open STAC item
item = pystac.Item.from_file("https://example.com/item.json")

# Access cloud-optimized data directly
with rasterio.open(item.assets["data"].href) as src:
    # Read only the data you need
    window = rasterio.windows.Window(0, 0, 512, 512)
    data = src.read(window=window)
```

### 2. Flexible Querying

STAC supports complex spatiotemporal queries:

```python
# Multi-dimensional search
search = catalog.search(
    # Spatial
    intersects=my_polygon,
    
    # Temporal
    datetime=["2024-01-01", "2024-12-31"],
    
    # Properties
    query={
        "eo:cloud_cover": {"lt": 20},
        "platform": {"in": ["landsat-8", "sentinel-2"]},
        "gsd": {"gte": 10, "lte": 30}
    },
    
    # Pagination
    limit=100
)
```

### 3. Asset Roles

STAC defines standard roles for assets:

| Role | Description | Example |
|------|-------------|---------|
| `data` | Primary data | GeoTIFF image |
| `metadata` | Metadata files | XML, JSON |
| `thumbnail` | Preview image | JPEG, PNG |
| `overview` | Reduced resolution | COG overview |
| `visual` | Visual representation | RGB composite |
| `data-mask` | Valid data mask | Binary mask |
| `snow-ice` | Snow/ice mask | Classification |
| `cloud` | Cloud mask | Cloud pixels |

### 4. Collection Summaries

Collections provide statistical summaries:

```json
"summaries": {
  "datetime": {
    "minimum": "2015-06-01T00:00:00Z",
    "maximum": "2024-01-01T00:00:00Z"
  },
  "eo:cloud_cover": {
    "minimum": 0,
    "maximum": 100
  },
  "instruments": ["oli", "tirs"],
  "gsd": [30],
  "eo:bands": [
    {"name": "B1", "common_name": "coastal", "center_wavelength": 0.44}
  ]
}
```

### 5. Link Relations

STAC uses standardized link relations:

```json
"links": [
  {"rel": "self", "href": "this-item.json"},
  {"rel": "parent", "href": "../collection.json"},
  {"rel": "collection", "href": "../collection.json"},
  {"rel": "root", "href": "../../catalog.json"},
  {"rel": "next", "href": "next-item.json"},
  {"rel": "derived_from", "href": "source-item.json"}
]
```

---

## STAC in the VEDA Platform

### VEDA's STAC Implementation

The **VEDA (Visualization, Exploration, and Data Analysis)** platform leverages STAC as its core data discovery and access mechanism. VEDA provides a comprehensive Earth data platform that makes NASA and other Earth science data accessible through standardized STAC interfaces.

### Key VEDA STAC Features

1. **Unified Data Catalog**
   - Single access point for multiple data collections
   - NASA EarthData integration
   - Community datasets

2. **STAC API Services**
   - Full STAC API implementation
   - Advanced search capabilities
   - Cloud-optimized data delivery

3. **Data Ingestion Pipeline**
   - Automated STAC metadata generation
   - Collection and item creation workflows
   - Quality control and validation

### VEDA STAC Collections

VEDA hosts various Earth observation collections:

```python
# Example VEDA collections
collections = [
    "nasa-disasters-flood-extent",
    "nasa-lis-global-lightning",
    "noaa-climate-normals",
    "blackmarble-nightlights",
    "air-quality-no2",
    "covid-19-economic-impact"
]
```

### Accessing VEDA STAC

```python
import pystac_client
from pystac_client import Client

# Connect to VEDA STAC API
veda_stac = Client.open("https://openveda.cloud/api/stac/")

# List available collections
for collection in veda_stac.get_collections():
    print(f"{collection.id}: {collection.title}")

# Search for specific data
search = veda_stac.search(
    collections=["air-quality-no2"],
    bbox=[-125, 25, -65, 50],  # Continental US
    datetime="2024-01-01/2024-01-31"
)

# Access results
items = list(search.items())
print(f"Found {len(items)} items")
```

### VEDA-Specific Notebooks

VEDA provides Jupyter notebooks for STAC operations:

1. **List STAC Collections**
   ```python
   # Explore available datasets
   from pystac_client import Client
   
   catalog = Client.open("https://openveda.cloud/api/stac/")
   collections = list(catalog.get_collections())
   
   for col in collections:
       print(f"ID: {col.id}")
       print(f"Title: {col.title}")
       print(f"Description: {col.description[:100]}...")
       print("---")
   ```

2. **Download STAC Assets**
   ```python
   import requests
   from pathlib import Path
   
   # Get item
   item = catalog.get_collection("collection-id").get_item("item-id")
   
   # Download asset
   asset = item.assets["data"]
   response = requests.get(asset.href)
   
   # Save locally
   Path("data.tif").write_bytes(response.content)
   ```

3. **Visualize STAC Data**
   ```python
   import folium
   from folium import plugins
   
   # Create map centered on item
   m = folium.Map(location=[item.bbox[1], item.bbox[0]], zoom_start=8)
   
   # Add item footprint
   folium.GeoJson(item.geometry).add_to(m)
   
   # Add tile layer if available
   if "visual" in item.assets:
       folium.raster_layers.TileLayer(
           tiles=item.assets["visual"].href
       ).add_to(m)
   
   m
   ```

### VEDA Data Discovery Patterns

1. **Temporal Analysis**
   ```python
   # Find all data for a specific event
   event_date = "2024-01-15"
   buffer_days = 7
   
   search = veda_stac.search(
       collections=["nasa-disasters-flood-extent"],
       datetime=f"{event_date}/+{buffer_days}days"
   )
   ```

2. **Spatial Analysis**
   ```python
   # Find data intersecting area of interest
   import geopandas as gpd
   
   aoi = gpd.read_file("study_area.geojson")
   
   search = veda_stac.search(
       intersects=aoi.geometry[0],
       collections=["blackmarble-nightlights"]
   )
   ```

3. **Multi-Collection Search**
   ```python
   # Compare multiple datasets
   collections = ["air-quality-no2", "covid-19-mobility"]
   
   results = {}
   for collection in collections:
       search = veda_stac.search(
           collections=[collection],
           bbox=bbox,
           datetime=datetime_range
       )
       results[collection] = list(search.items())
   ```

---

## Working with STAC APIs

### Basic API Requests

```python
import requests

# Base URL for STAC API
stac_api = "https://openveda.cloud/api/stac"

# Get landing page
response = requests.get(f"{stac_api}/")
landing_page = response.json()

# List collections
response = requests.get(f"{stac_api}/collections")
collections = response.json()["collections"]

# Get specific collection
response = requests.get(f"{stac_api}/collections/air-quality-no2")
collection = response.json()

# Search items
search_params = {
    "bbox": [-125, 25, -65, 50],
    "datetime": "2024-01-01/2024-01-31",
    "collections": ["air-quality-no2"],
    "limit": 10
}
response = requests.post(f"{stac_api}/search", json=search_params)
search_results = response.json()
```

### Advanced Search Features

#### CQL2 Filtering
```python
# Complex query using CQL2
cql2_filter = {
    "op": "and",
    "args": [
        {
            "op": ">=",
            "args": [{"property": "eo:cloud_cover"}, 0]
        },
        {
            "op": "<=",
            "args": [{"property": "eo:cloud_cover"}, 10]
        },
        {
            "op": "in",
            "args": [
                {"property": "platform"},
                ["landsat-8", "landsat-9"]
            ]
        }
    ]
}

search_body = {
    "filter": cql2_filter,
    "limit": 100
}
```

#### Sorting Results
```python
search_params = {
    "sortby": [
        {"field": "properties.datetime", "direction": "desc"},
        {"field": "properties.eo:cloud_cover", "direction": "asc"}
    ]
}
```

#### Field Selection
```python
# Return only specific fields
search_params = {
    "fields": {
        "include": ["id", "properties.datetime", "assets.data"],
        "exclude": ["geometry", "links"]
    }
}
```

---

## Python Libraries for STAC

### Core Libraries

1. **PySTAC** - Read and write STAC catalogs
   ```bash
   pip install pystac
   ```

2. **PySTAC Client** - Search STAC APIs
   ```bash
   pip install pystac-client
   ```

3. **STAC Browser** - Web interface for browsing
   ```bash
   # Docker deployment
   docker run -p 8080:8080 radiantearth/stac-browser
   ```

### Data Processing Libraries

```python
# Stack of libraries for STAC data processing
pip install pystac pystac-client rasterio xarray rioxarray geopandas folium stackstac odc-stac
```

### Library Examples

#### PySTAC - Catalog Creation
```python
import pystac
from datetime import datetime

# Create catalog
catalog = pystac.Catalog(
    id="my-catalog",
    description="My Earth observation catalog"
)

# Create collection
collection = pystac.Collection(
    id="my-collection",
    description="My data collection",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent([[-180, -90, 180, 90]]),
        temporal=pystac.TemporalExtent([[datetime(2024, 1, 1), None]])
    )
)

# Add collection to catalog
catalog.add_child(collection)

# Save catalog
catalog.normalize_and_save("./my-catalog")
```

#### StackSTAC - Create xarray from STAC
```python
import stackstac
import pystac_client

# Search for data
catalog = pystac_client.Client.open("https://openveda.cloud/api/stac/")
items = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 37.5, -122, 38],
    datetime="2024-01-01/2024-01-31"
).item_collection()

# Create xarray DataArray
stack = stackstac.stack(
    items,
    assets=["B04", "B03", "B02"],  # RGB bands
    resolution=10,
    bounds_latlon=[-122.5, 37.5, -122, 38]
)

print(stack)
# <xarray.DataArray (time: 5, band: 3, y: 5000, x: 5000)>
```

#### ODC-STAC - Load into Open Data Cube
```python
import odc.stac
import pystac_client

# Search catalog
catalog = pystac_client.Client.open("https://openveda.cloud/api/stac/")
items = list(catalog.search(
    collections=["landsat-c2-l2"],
    bbox=[149, -36, 150, -35],
    datetime="2024-01"
).items())

# Load into xarray
data = odc.stac.load(
    items,
    bands=["red", "green", "blue"],
    resolution=30,
    crs="EPSG:3857"
)
```

---

## Practical Examples

### Example 1: Disaster Response - Flood Monitoring

```python
import pystac_client
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Connect to VEDA STAC
client = pystac_client.Client.open("https://openveda.cloud/api/stac/")

# Define area of interest (e.g., flood zone)
flood_area = {
    "type": "Polygon",
    "coordinates": [[
        [-95.5, 29.5], [-95.5, 30.0],
        [-95.0, 30.0], [-95.0, 29.5],
        [-95.5, 29.5]
    ]]
}

# Search for pre and post flood imagery
flood_date = datetime(2024, 1, 15)

# Pre-flood
pre_search = client.search(
    collections=["sentinel-2-l2a"],
    intersects=flood_area,
    datetime=[(flood_date - timedelta(days=10)).isoformat(),
              (flood_date - timedelta(days=1)).isoformat()],
    query={"eo:cloud_cover": {"lt": 20}}
)

# Post-flood
post_search = client.search(
    collections=["sentinel-2-l2a"],
    intersects=flood_area,
    datetime=[flood_date.isoformat(),
              (flood_date + timedelta(days=10)).isoformat()],
    query={"eo:cloud_cover": {"lt": 20}}
)

pre_items = list(pre_search.items())
post_items = list(post_search.items())

print(f"Found {len(pre_items)} pre-flood images")
print(f"Found {len(post_items)} post-flood images")

# Process and compare imagery
# ... (additional processing code)
```

### Example 2: Time Series Analysis

```python
import pystac_client
import pandas as pd
import matplotlib.pyplot as plt

# Connect to catalog
client = pystac_client.Client.open("https://openveda.cloud/api/stac/")

# Location of interest
point = {"type": "Point", "coordinates": [-122.4, 37.8]}  # San Francisco

# Search for time series
search = client.search(
    collections=["air-quality-no2"],
    intersects=point,
    datetime="2023-01-01/2024-01-01"
)

# Collect data
dates = []
values = []

for item in search.items():
    dates.append(pd.to_datetime(item.properties["datetime"]))
    # Extract value (simplified - actual extraction depends on data format)
    values.append(item.properties.get("no2_concentration", 0))

# Create time series
ts = pd.Series(values, index=dates)
ts = ts.sort_index()

# Plot
plt.figure(figsize=(12, 6))
ts.plot(title="NO2 Concentration Time Series - San Francisco")
plt.ylabel("NO2 Concentration")
plt.xlabel("Date")
plt.grid(True, alpha=0.3)
plt.show()

# Calculate statistics
print(f"Mean: {ts.mean():.2f}")
print(f"Max: {ts.max():.2f}")
print(f"Min: {ts.min():.2f}")
```

### Example 3: Multi-Source Data Fusion

```python
import pystac_client
import numpy as np
from rasterio import features
import geopandas as gpd

# Connect to multiple STAC catalogs
veda = pystac_client.Client.open("https://openveda.cloud/api/stac/")
planetary = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

# Area and time of interest
bbox = [-122.5, 37.5, -122, 38]
date_range = "2024-01-01/2024-01-31"

# Search multiple sources
datasets = {}

# VEDA data
veda_search = veda.search(
    collections=["air-quality-no2"],
    bbox=bbox,
    datetime=date_range
)
datasets["air_quality"] = list(veda_search.items())

# Planetary Computer data
pc_search = planetary.search(
    collections=["landsat-c2-l2"],
    bbox=bbox,
    datetime=date_range
)
datasets["landsat"] = list(pc_search.items())

# Combine datasets for analysis
print("Data sources found:")
for source, items in datasets.items():
    print(f"  {source}: {len(items)} items")

# Spatial join example
air_quality_gdf = gpd.GeoDataFrame(
    [{"id": item.id, "datetime": item.datetime, "geometry": shape(item.geometry)}
     for item in datasets["air_quality"]]
)

landsat_gdf = gpd.GeoDataFrame(
    [{"id": item.id, "datetime": item.datetime, "geometry": shape(item.geometry)}
     for item in datasets["landsat"]]
)

# Find overlapping data
overlaps = air_quality_gdf.sjoin(landsat_gdf, how="inner", predicate="intersects")
print(f"Found {len(overlaps)} overlapping scenes")
```

---

## STAC Best Practices

### 1. Catalog Organization

```
Best Practice Structure:
catalog/
├── catalog.json
├── collections/
│   ├── landsat-8/
│   │   ├── collection.json
│   │   └── items/
│   │       ├── 2024-01/
│   │       │   ├── item1.json
│   │       │   └── item2.json
│   │       └── 2024-02/
│   └── sentinel-2/
└── extensions/
```

### 2. Metadata Standards

```python
# Always include these essential properties
item_properties = {
    "datetime": "2024-01-15T10:30:00Z",  # ISO 8601
    "created": "2024-01-15T12:00:00Z",
    "updated": "2024-01-15T12:00:00Z",
    "license": "CC-BY-4.0",
    "providers": [
        {
            "name": "Organization Name",
            "roles": ["producer", "processor"],
            "url": "https://organization.com"
        }
    ]
}
```

### 3. Asset Best Practices

```python
# Use Cloud-Optimized formats
assets = {
    "data": {
        "href": "https://storage.com/data.tif",
        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
        "roles": ["data"],
        "title": "Cloud Optimized GeoTIFF",
        # Include key metadata
        "proj:epsg": 4326,
        "raster:bands": [
            {
                "data_type": "uint16",
                "nodata": 0,
                "statistics": {
                    "minimum": 0,
                    "maximum": 10000,
                    "mean": 5000,
                    "stddev": 1500
                }
            }
        ]
    }
}
```

### 4. Search Optimization

```python
# Efficient searching strategies

# 1. Use spatial and temporal indexes
search = catalog.search(
    bbox=small_bbox,  # Start with smaller area
    datetime=specific_date,  # Narrow time range
    limit=10  # Use pagination
)

# 2. Filter early
search = catalog.search(
    collections=["specific-collection"],  # Limit collections
    query={"eo:cloud_cover": {"lt": 10}},  # Apply filters
    max_items=100  # Set maximum
)

# 3. Use field selection
search = catalog.search(
    fields={
        "include": ["id", "properties.datetime", "assets.data.href"],
        "exclude": ["geometry"]  # Exclude large fields if not needed
    }
)
```

### 5. Validation

```python
import pystac
from pystac.validation import validate_dict

# Validate STAC objects
item = pystac.Item.from_file("item.json")

# Validate against schema
try:
    item.validate()
    print("Item is valid!")
except pystac.STACValidationError as e:
    print(f"Validation error: {e}")

# Use STAC Validator tool
# pip install stac-validator
from stac_validator import stac_validator

validator = stac_validator.StacValidator()
valid = validator.validate_file("catalog.json")
```

---

## Resources and Links

### Official STAC Resources

- **STAC Specification**: [https://stacspec.org](https://stacspec.org)
- **STAC Index** (Catalogs & Tools): [https://stacindex.org](https://stacindex.org)
- **STAC GitHub**: [https://github.com/radiantearth/stac-spec](https://github.com/radiantearth/stac-spec)
- **STAC Gitter Chat**: [https://gitter.im/SpatioTemporal-Asset-Catalog/community](https://gitter.im/SpatioTemporal-Asset-Catalog/community)
- **STAC Google Group**: [https://groups.google.com/g/stac-spec](https://groups.google.com/g/stac-spec)

### VEDA Platform Resources

- **VEDA Documentation**: [https://docs.openveda.cloud/](https://docs.openveda.cloud/)
- **VEDA STAC API**: [https://openveda.cloud/api/stac/](https://openveda.cloud/api/stac/)
- **VEDA GitHub**: [https://github.com/NASA-IMPACT/veda-data](https://github.com/NASA-IMPACT/veda-data)
- **VEDA Jupyter Examples**: Available in VEDA JupyterHub instances

### Python Libraries

- **PySTAC**: [https://pystac.readthedocs.io](https://pystac.readthedocs.io)
- **PySTAC Client**: [https://pystac-client.readthedocs.io](https://pystac-client.readthedocs.io)
- **StackSTAC**: [https://stackstac.readthedocs.io](https://stackstac.readthedocs.io)
- **ODC-STAC**: [https://odc-stac.readthedocs.io](https://odc-stac.readthedocs.io)
- **STAC-validator**: [https://github.com/stac-utils/stac-validator](https://github.com/stac-utils/stac-validator)

### Public STAC Catalogs

- **Microsoft Planetary Computer**: [https://planetarycomputer.microsoft.com/catalog](https://planetarycomputer.microsoft.com/catalog)
- **AWS Earth on AWS**: [https://earth-search.aws.element84.com/v1](https://earth-search.aws.element84.com/v1)
- **Google Earth Engine**: [https://earthengine-stac.storage.googleapis.com/catalog/catalog.json](https://earthengine-stac.storage.googleapis.com/catalog/catalog.json)
- **NASA CMR STAC**: [https://cmr.earthdata.nasa.gov/stac](https://cmr.earthdata.nasa.gov/stac)
- **USGS STAC**: [https://landsatlook.usgs.gov/stac-server](https://landsatlook.usgs.gov/stac-server)

### Tools and Utilities

- **STAC Browser**: [https://radiantearth.github.io/stac-browser](https://radiantearth.github.io/stac-browser)
- **STAC Validator**: [https://staclint.com](https://staclint.com)
- **STAC API Validator**: [https://github.com/stac-utils/stac-api-validator](https://github.com/stac-utils/stac-api-validator)
- **QGIS STAC Plugin**: [https://github.com/stac-utils/qgis-stac-plugin](https://github.com/stac-utils/qgis-stac-plugin)
- **DotNetStac** (.NET): [https://github.com/Terradue/DotNetStac](https://github.com/Terradue/DotNetStac)
- **stac4s** (Scala): [https://github.com/azavea/stac4s](https://github.com/azavea/stac4s)

### Learning Resources

#### Tutorials
- **STAC Tutorials**: [https://stacspec.org/en/tutorials/](https://stacspec.org/en/tutorials/)
- **Cloud Native Geospatial**: [https://cloudnativegeo.org](https://cloudnativegeo.org)
- **PySTAC Tutorial**: [https://pystac.readthedocs.io/en/stable/tutorials.html](https://pystac.readthedocs.io/en/stable/tutorials.html)

#### Videos
- **STAC Overview (YouTube)**: Search "STAC specification introduction"
- **FOSS4G Presentations**: Annual conference talks on STAC
- **Cloud-Native Geospatial Webinars**: Regular community events

#### Courses
- **Cloud-Native Geospatial Academy**: [https://academy.cloudnativegeo.org](https://academy.cloudnativegeo.org)
- **NASA ARSET Training**: Includes STAC modules
- **OGC Training**: OpenGIS Consortium resources

### Community and Support

- **STAC Gitter Chat**: Real-time community support
- **GitHub Discussions**: Technical discussions and Q&A
- **Stack Overflow**: Tag: `stac` or `spatio-temporal-asset-catalog`
- **Twitter/X**: Follow @STACspec for updates

### Related Standards

- **OGC API - Features**: [https://ogcapi.ogc.org/features/](https://ogcapi.ogc.org/features/)
- **Cloud Optimized GeoTIFF**: [https://www.cogeo.org](https://www.cogeo.org)
- **Zarr**: [https://zarr.dev](https://zarr.dev)
- **GeoParquet**: [https://geoparquet.org](https://geoparquet.org)
- **Cloud Optimized Point Cloud**: [https://copc.io](https://copc.io)

---

## Quick Reference Card

### Common STAC Operations

```python
# Setup
from pystac_client import Client
import pystac

# Connect to catalog
catalog = Client.open("https://example.com/stac/")

# List collections
for collection in catalog.get_collections():
    print(collection.id)

# Search items
search = catalog.search(
    collections=["collection-id"],
    bbox=[-180, -90, 180, 90],
    datetime="2024-01-01/2024-12-31",
    limit=100
)

# Get items
items = list(search.items())

# Access item properties
for item in items:
    print(f"ID: {item.id}")
    print(f"Date: {item.datetime}")
    print(f"Bbox: {item.bbox}")
    print(f"Assets: {list(item.assets.keys())}")

# Download asset
import requests
asset_url = items[0].assets["data"].href
response = requests.get(asset_url)
with open("data.tif", "wb") as f:
    f.write(response.content)

# Create new item
item = pystac.Item(
    id="my-item",
    geometry={...},
    bbox=[...],
    datetime=datetime.now(),
    properties={},
    assets={}
)

# Validate
item.validate()
```

---

*Last Updated: 2024*  
*Version: 1.0*  
*STAC Training Guide for VEDA Platform*

For the latest updates and additional resources, visit:
- VEDA Documentation: [https://docs.openveda.cloud/](https://docs.openveda.cloud/)
- STAC Specification: [https://stacspec.org](https://stacspec.org)