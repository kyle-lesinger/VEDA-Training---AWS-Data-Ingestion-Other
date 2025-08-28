# Regular Expressions (Regex) Guide for Geospatial File Patterns

## Table of Contents
1. [Introduction](#introduction)
2. [Essential Tool - regex101.com](#essential-tool---regex101com)
3. [Basic Regex Syntax](#basic-regex-syntax)
4. [Filename Patterns for Geospatial Data](#filename-patterns-for-geospatial-data)
5. [VEDA File Naming Standards](#veda-file-naming-standards)
6. [Common Date Patterns in Filenames](#common-date-patterns-in-filenames)
7. [S3 and Cloud Storage Patterns](#s3-and-cloud-storage-patterns)
8. [Testing Your Patterns](#testing-your-patterns)
9. [Python Implementation](#python-implementation)
10. [Quick Reference](#quick-reference)

---

## Introduction

Regular expressions (regex) are pattern-matching tools essential for working with geospatial data files. In data pipelines, regex helps you:
- Identify and validate file naming conventions
- Extract dates from filenames
- Filter specific datasets
- Automate file organization

This guide focuses on **filename patterns** commonly used in Earth observation and climate data.

---

## Essential Tool - regex101.com

### 🔧 Always Use [regex101.com](https://regex101.com/)

**[regex101.com](https://regex101.com/)** is your essential companion for testing regex patterns. Before using any pattern in production:

1. Go to **[regex101.com](https://regex101.com/)**
2. Select **Python** as the flavor (for VEDA/GHG Center work)
3. Paste sample filenames in the test area
4. Build and test your pattern
5. Use the explanation panel to understand each part

### Quick Start Example

Try this at [regex101.com](https://regex101.com/):
- Test String: `landsat9_20251007.tif`
- Pattern: `landsat\d_(\d{8})\.tif`
- Result: Matches! Captures date: `20251007`

---

## Basic Regex Syntax

### Essential Characters for Filename Matching

| Pattern | Description | Example | Matches |
|---------|-------------|---------|---------|
| `\d` | Any digit (0-9) | `\d{4}` | `2024` |
| `\w` | Letters, digits, underscore | `\w+` | `landsat_9` |
| `.` | Any character | `.*` | anything |
| `\.` | Literal period | `\.tif` | `.tif` |
| `_` | Literal underscore | `data_` | `data_` |
| `-` | Literal hyphen | `2024-01` | `2024-01` |
| `[abc]` | Any of a, b, or c | `[0-9]` | any digit |
| `^` | Start of string | `^landsat` | starts with landsat |
| `$` | End of string | `\.tif$` | ends with .tif |

### Quantifiers

| Pattern | Description | Example |
|---------|-------------|---------|
| `{n}` | Exactly n | `\d{8}` matches `20240115` |
| `{n,m}` | Between n and m | `\d{2,4}` matches `24` or `2024` |
| `+` | One or more | `\w+` matches `landsat` |
| `*` | Zero or more | `v\d*` matches `v` or `v123` |
| `?` | Zero or one | `v?\d` matches `1` or `v1` |

### Capture Groups

| Pattern | Description | Example |
|---------|-------------|---------|
| `()` | Capture group | `(\d{4})-(\d{2})` captures year and month |
| `(?:)` | Non-capturing group | `(?:landsat\|sentinel)` matches but doesn't capture |
| `\1` | Backreference | `(\d{2})-\1` matches `12-12` |

**Test all patterns at [regex101.com](https://regex101.com/)**

---

## Filename Patterns for Geospatial Data

### Satellite Data Files

```regex
# Landsat files
^landsat[89]_(\d{8})\.tif$
# Matches: landsat8_20240115.tif, landsat9_20251007.tif

# Sentinel-2 files
^S2[AB]_.*_(\d{8}T\d{6})_.*\.tif$
# Matches: S2A_MSIL1C_20240115T101031_N0510_R022_T32UNE.tif

# MODIS files
^MOD\d{2}[A-Z]\d\.A(\d{7})\..*\.tif$
# Matches: MOD09GA.A2024015.h08v05.061.tif

# VIIRS files
^VNP\d{2}.*\.A(\d{7})\.(\d{4})\..*\.tif$
# Matches: VNP09GA.A2024015.1800.001.tif
```

### Climate Model Output

```regex
# CMIP6 format
^(\w+)_(\w+)_(\w+)_(\w+)_(\w+)_(\d{6})-(\d{6})\.nc$
# Matches: tas_Amon_GFDL-ESM4_historical_r1i1p1f1_185001-201412.nc

# ERA5 reanalysis
^era5_(\w+)_(\d{4})(\d{2})\.nc$
# Matches: era5_temperature_202401.nc
```

### Processed COG Files

```regex
# Standard COG naming
^(\w+)_(\d{8})_cog\.tif$
# Matches: ndvi_20240115_cog.tif

# Versioned COGs
^(\w+)_v(\d+\.\d+\.\d+)_(\d{8})\.tif$
# Matches: precipitation_v2.1.0_20240115.tif
```

---

## VEDA File Naming Standards

### 📚 Official VEDA Documentation

**Always refer to the [VEDA File Preparation Guidelines](https://docs.openveda.cloud/user-guide/content-curation/dataset-ingestion/file-preparation.html) for official naming conventions.**

### VEDA-Compliant Patterns

According to VEDA standards, COG files should follow specific naming conventions:

```regex
# Basic VEDA pattern
^[a-z0-9][a-z0-9_-]*_(\d{4}|\d{6}|\d{8})\.tif$
# Requirements:
# - Lowercase letters and numbers only
# - Underscores or hyphens as separators
# - Date component (YYYY, YYYYMM, or YYYYMMDD)
# - .tif extension

# Examples that match VEDA standards:
# ✅ ghg_emissions_20240115.tif
# ✅ temperature_anomaly_202401.tif
# ✅ ndvi_composite_2024.tif

# Examples that DON'T match:
# ❌ GHG_Emissions_20240115.tif (uppercase)
# ❌ ghg.emissions.20240115.tif (dots)
# ❌ ghg-emissions-2024-01-15.tif (date format)
```

### Collection-Specific Patterns

```regex
# ODIAC CO2 emissions
^odiac\d{4}_1km_excl_intl_(\d{6})\.tif$
# Matches: odiac2023_1km_excl_intl_202401.tif

# EPA CH4 emissions
^epa_ch4_express_.*_(\d{4})\.tif$
# Matches: epa_ch4_express_grid_2024.tif

# EMIT methane plumes
^emit_ch4plume_.*_(\d{8}T\d{6})\.tif$
# Matches: emit_ch4plume_california_20240115T143022.tif
```

**Test these patterns at [regex101.com](https://regex101.com/) with your actual filenames!**

---

## Common Date Patterns in Filenames

### Date Formats

```regex
# YYYYMMDD (most common)
(\d{8})
# Matches: 20240115, 20251007
# Example: landsat9_20251007.tif

# YYYY-MM-DD
(\d{4})-(\d{2})-(\d{2})
# Matches: 2024-01-15
# Example: data_2024-01-15.tif

# YYYYMM
(\d{6})
# Matches: 202401
# Example: monthly_avg_202401.tif

# YYYY only
(\d{4})
# Matches: 2024
# Example: annual_total_2024.tif

# Julian day (YYYYDDD)
(\d{4})(\d{3})
# Matches: 2024015 (day 15 of 2024)
# Example: modis_2024015.tif

# With timestamp (YYYYMMDDTHHMMSS)
(\d{8})T(\d{6})
# Matches: 20240115T143022
# Example: snapshot_20240115T143022.tif
```

### Extracting Dates from Various Filename Formats

```regex
# Flexible date extraction
.*(\d{4})[-_]?(\d{2})[-_]?(\d{2}).*
# Captures year, month, day from various formats:
# landsat_2024_01_15_processed.tif
# data-2024-01-15.tif
# 20240115_temperature.tif

# Date at end of filename (before extension)
.*_(\d{8})\.tif$
# Matches: anything_20240115.tif

# Date at beginning
^(\d{8})_.*\.tif$
# Matches: 20240115_anything.tif

# Date with prefix
^[a-z]+_(\d{8})\.tif$
# Matches: temperature_20240115.tif
```

### Real-World Examples

Test these at [regex101.com](https://regex101.com/):

```
Filenames to test:
- landsat9_20251007.tif
- sentinel2_20240115_processed.tif
- MOD09GA.A2024015.h08v05.tif
- temperature_monthly_202401.tif
- precip_daily_2024-01-15.tif
- ghg_emissions_20240115T143022.tif
```

---

## S3 and Cloud Storage Patterns

### S3 Path Patterns

```regex
# Full S3 URI
^s3://([^/]+)/(.+)$
# Captures: bucket name and key
# Example: s3://ghgc-data-store/odiac/2024/data.tif

# S3 key with date folders
^(\w+)/(\d{4})/(\d{2})/(.+\.tif)$
# Matches: odiac/2024/01/odiac_20240115.tif

# Versioned S3 paths
^(\w+)/v(\d+\.\d+\.\d+)/(.+)$
# Matches: dataset/v2.1.0/file.tif
```

### Data Organization Patterns

```regex
# Year/Month/Day structure
(\d{4})/(\d{2})/(\d{2})/(.+)
# Matches: 2024/01/15/data.tif

# Collection/Year/File
^([a-z0-9_-]+)/(\d{4})/([a-z0-9_-]+\.tif)$
# Matches: ghg_emissions/2024/emissions_20240115.tif
```

---

## Testing Your Patterns

### Step-by-Step Testing at regex101.com

1. **Go to [regex101.com](https://regex101.com/)**
2. **Select Python flavor**
3. **Paste your test filenames:**
   ```
   landsat9_20251007.tif
   landsat8_20240615.tif
   sentinel2_20240115.tif
   landsat7_invalid.tif
   ```
4. **Build your pattern:**
   ```regex
   ^landsat[89]_(\d{8})\.tif$
   ```
5. **Check matches and captures**
6. **Save and share your pattern**

### Validation Checklist

- ✅ Does it match valid filenames?
- ✅ Does it reject invalid filenames?
- ✅ Does it capture the right date/version?
- ✅ Is it compatible with VEDA standards?
- ✅ Test at [regex101.com](https://regex101.com/)

---

## Python Implementation

### Basic File Matching

```python
import re
from pathlib import Path

# Define pattern for Landsat files
pattern = re.compile(r'^landsat[89]_(\d{8})\.tif$')

# Test filenames
filenames = [
    'landsat9_20251007.tif',
    'landsat8_20240615.tif',
    'sentinel2_20240115.tif'
]

for filename in filenames:
    match = pattern.match(filename)
    if match:
        date = match.group(1)
        print(f"✅ {filename} - Date: {date}")
    else:
        print(f"❌ {filename} - No match")
```

### Batch File Processing

```python
import re
import os
from datetime import datetime

def extract_date_from_filename(filename):
    """Extract date from various filename formats"""
    patterns = [
        (r'.*_(\d{8})\.tif$', '%Y%m%d'),      # YYYYMMDD
        (r'.*_(\d{6})\.tif$', '%Y%m'),        # YYYYMM
        (r'.*_(\d{4})\.tif$', '%Y'),          # YYYY
        (r'.*_(\d{4})-(\d{2})-(\d{2}).*', 'split')  # YYYY-MM-DD
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, filename)
        if match:
            if date_format == 'split':
                year, month, day = match.groups()
                return datetime(int(year), int(month), int(day))
            else:
                return datetime.strptime(match.group(1), date_format)
    
    return None

# Example usage
files = [
    'landsat9_20251007.tif',
    'monthly_avg_202401.tif',
    'annual_total_2024.tif',
    'data_2024-01-15_processed.tif'
]

for file in files:
    date = extract_date_from_filename(file)
    if date:
        print(f"{file} -> {date.strftime('%Y-%m-%d')}")
```

### S3 Key Filtering

```python
import re
import boto3

def filter_s3_keys_by_date_range(bucket, prefix, start_date, end_date):
    """Filter S3 keys by date range using regex"""
    s3 = boto3.client('s3')
    pattern = re.compile(r'.*_(\d{8})\.tif$')
    
    matching_keys = []
    
    # List objects
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        match = pattern.search(key)
        
        if match:
            file_date = match.group(1)
            if start_date <= file_date <= end_date:
                matching_keys.append(key)
    
    return matching_keys

# Example
keys = filter_s3_keys_by_date_range(
    bucket='ghgc-data-store',
    prefix='landsat/',
    start_date='20240101',
    end_date='20241231'
)
```

---

## Quick Reference

### Most Common Filename Patterns

```regex
# Landsat with date
landsat[89]_(\d{8})\.tif

# Any satellite with date
^[a-z]+\d?_(\d{8})\.tif$

# Monthly data files
^[a-z_]+_(\d{6})\.tif$

# Annual data files
^[a-z_]+_(\d{4})\.tif$

# Versioned files
^[a-z_]+_v(\d+\.\d+\.\d+)_.*\.tif$

# VEDA-compliant COG
^[a-z0-9][a-z0-9_-]*_\d{4,8}\.tif$

# S3 path with date folders
s3://[^/]+/\d{4}/\d{2}/[^/]+\.tif$

# Any .tif file
.*\.tif$

# Files with specific extensions
\.(tif|tiff|nc|hdf|zarr)$
```

**Always validate patterns at [regex101.com](https://regex101.com/) before using in production!**

---

## Best Practices

1. **Follow VEDA Standards**
   - Check [VEDA File Preparation Guide](https://docs.openveda.cloud/user-guide/content-curation/dataset-ingestion/file-preparation.html)
   - Use lowercase letters and numbers
   - Include clear date components

2. **Test Thoroughly**
   - Always test at [regex101.com](https://regex101.com/)
   - Include edge cases in testing
   - Verify date extraction works correctly

3. **Keep Patterns Simple**
   - Start with basic patterns
   - Add complexity only when needed
   - Document complex patterns

4. **Performance Considerations**
   - Compile patterns that are used repeatedly
   - Use specific patterns over wildcards
   - Avoid excessive backtracking

---

## Additional Resources

- **[regex101.com](https://regex101.com/)** - Essential testing tool
- **[VEDA File Standards](https://docs.openveda.cloud/user-guide/content-curation/dataset-ingestion/file-preparation.html)** - Official naming conventions
- **[Python re module](https://docs.python.org/3/library/re.html)** - Python regex documentation
- **[RegexOne Tutorial](https://regexone.com/)** - Interactive learning

---

*Remember: Always test your patterns at [regex101.com](https://regex101.com/) and follow [VEDA file naming standards](https://docs.openveda.cloud/user-guide/content-curation/dataset-ingestion/file-preparation.html)!*

*Last Updated: 2024*