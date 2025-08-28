# VEDA and NASA ASDC File Naming Conventions Comparison

## Table of Contents
1. [VEDA File Naming Standards](#veda-file-naming-standards)
2. [NASA ASDC File Naming Standards](#nasa-asdc-file-naming-standards)
3. [Comparison and Analysis](#comparison-and-analysis)
4. [Best Practices](#best-practices)
5. [Quick Reference](#quick-reference)

---

## VEDA File Naming Standards

### Overview
VEDA (Visualization, Exploration, and Data Analysis) platform requires Cloud-Optimized GeoTIFF (COG) files to follow specific naming conventions for proper ingestion and cataloging.

**Official Documentation**: [VEDA File Preparation Guidelines](https://docs.openveda.cloud/user-guide/content-curation/dataset-ingestion/file-preparation.html)

### Core Requirements

1. **File Extension**: Must be `.tif` for Cloud-Optimized GeoTIFFs
2. **Datetime Prefix**: Always precede datetime with an underscore `_`
3. **Character Set**: Use lowercase letters, numbers, underscores, and hyphens
4. **Descriptive Names**: Use meaningful, descriptive filenames

### Datetime Format Options

#### Single Datetime Values

| Granularity | Format Examples |
|------------|-----------------|
| **Year** | `nightlights_2012.tif`<br>`nightlights_2012-yearly.tif` |
| **Month** | `nightlights_201201.tif`<br>`nightlights_2012-01_monthly.tif` |
| **Day** | `nightlights_20120101day.tif`<br>`nightlights_2012-01-01_day.tif` |
| **Sub-daily** | `TEMPO_NO2_L3_V03_2024-04-11T19:09:53Z.tif`<br>`TEMPO_NO2_L3_V03_20240411T19:09:53Z.tif` |

#### Datetime Ranges

| Granularity | Format Examples |
|------------|-----------------|
| **Year Range** | `nightlights_2012_2014.tif` |
| **Month Range** | `nightlights_201201_201205.tif` |
| **Day Range** | `nightlights_20120101day_20121221.tif` |

### Real-World VEDA Examples

```
# ODIAC CO2 Emissions
odiac2023_1km_excl_intl_202301.tif
odiac2023_1km_excl_intl_202312.tif

# EPA CH4 Emissions
epa_ch4_express_grid_2024.tif
epa_ch4_express_landfills_2024.tif

# EMIT Methane Plumes
emit_ch4plume_california_20240115T143022.tif
emit_ch4plume_permian_20240210T095430.tif

# Temperature Anomalies
temperature_anomaly_global_202401.tif
temperature_anomaly_global_2024.tif

# Landsat Data
landsat9_20251007.tif
landsat8_ndvi_20240615.tif
```

### VEDA Pattern Rules

```regex
# Basic VEDA-compliant pattern
^[a-z0-9][a-z0-9_-]*_(\d{4}|\d{6}|\d{8})\.tif$

# With ISO timestamp
^[A-Z0-9_]+_(\d{8}T\d{6}Z?)\.tif$

# With date range
^[a-z0-9_-]+_(\d{4,8})_(\d{4,8})\.tif$
```

---

## NASA ASDC File Naming Standards

### Overview
NASA Atmospheric Science Data Center (ASDC) uses a structured naming convention for GEWEX Radiative Flux Assessment (RFA) data products.

**Official Documentation**: [NASA ASDC Data Format Standards](https://asdc.larc.nasa.gov/documents/gewex-rfa/documents/data_format.html#file_naming)

### File Name Structure

```
<ProductName>_<ProductVersion>_<DataDescriptors>_<TimeTag>_<RFAVersion>.<Extension>
```

### Component Definitions

#### 1. ProductName
- Unique product identifier
- Relates to original archived dataset
- Append "-MOD" for modified/experimental data

#### 2. ProductVersion
- Format: `Edccc` (alphanumeric)
- Examples: `Ed01a`, `Ed02b`, `EdXXX`

#### 3. DataDescriptors
Components concatenated with hyphens:
- **Data Category**: TOA (Top of Atmosphere), SFC (Surface), etc.
- **Data Subcategory**: MAP (Mapped), TS (Time Series), etc.
- **Time Interval**: MON (Monthly), DAY (Daily), HR (Hourly)
- **Spatial Area**: GLOB (Global), specific regions
- **Parameter**: Physical parameter code

#### 4. TimeTag
- Format: `YYYYMMDDHH` for single time
- Format: `YYYYMMDDHH-YYYYMMDDHH` for time range
- Use "99" for unspecified fields

#### 5. RFAVersion
- Format: `RFAnn` (incremental integer)
- Examples: `RFA01`, `RFA02`

#### 6. Extension
- Allowed: `.txt`, `.asc`, `.png`, `.gif`, `.jpg`, `.tiff`, `.tif`

### Real-World NASA ASDC Examples

```
# Satellite Data
CERESTISA_Ed01a_TOA-MAP-MON-GLOB-ASWUP_2002019999_RFA01.asc
ISCCP-MOD_Ed031_SFC-MAP-DAY-GLOB-ATOTNET_1999050101_RFA02.asc
GEWEX-SRB_Ed30c_SFC-MAP-MON-GLOB-ASWDN_2007079999_RFA01.tif

# Ground-based Data
BSRN_EdXXX_MEA-TS-MON-BAR-ASWDN_2003019999-2003129999_RFA01.asc
SURFRAD_Ed01a_MEA-TS-HR-BON-ALWUP_2001010100-2001123123_RFA01.txt

# Modified Products
CERES-MOD_Ed02b_TOA-MAP-DAY-NPOL-ALWDN_2010010199_RFA03.tif
```

---

## Comparison and Analysis

### Similarities Between VEDA and NASA ASDC

| Aspect | Similarity |
|--------|------------|
| **Date/Time Inclusion** | Both require temporal information in filename |
| **Underscore Separator** | Both use underscores as primary separator |
| **Descriptive Content** | Both emphasize meaningful, descriptive names |
| **File Extensions** | Both support `.tif` for GeoTIFF files |
| **Structured Format** | Both follow predictable patterns |
| **Version Support** | Both can include version information |

### Key Differences

| Aspect | VEDA | NASA ASDC |
|--------|------|-----------|
| **Case Sensitivity** | Lowercase preferred | Mixed case allowed |
| **Structure Rigidity** | Flexible format | Fixed component order |
| **Date Format** | Multiple formats (YYYY, YYYYMM, YYYYMMDD) | Fixed YYYYMMDDHH |
| **Separators** | Underscores and hyphens | Underscores between components, hyphens within |
| **Version Format** | Simple (v1.0, v2.1.0) | Structured (Edccc, RFAnn) |
| **Metadata Encoding** | Minimal in filename | Extensive metadata in filename |
| **Complexity** | Simple and readable | Complex but systematic |
| **ISO8601 Support** | Yes (with T separator) | No |

### Format Comparison Examples

| Dataset Type | VEDA Format | NASA ASDC Format |
|-------------|-------------|------------------|
| Monthly Temperature | `temperature_202401.tif` | `TEMP_Ed01a_SFC-MAP-MON-GLOB-TEMP_2024019999_RFA01.tif` |
| Daily Precipitation | `precip_20240115.tif` | `PRECIP_Ed01a_SFC-MAP-DAY-GLOB-PRCP_2024011599_RFA01.tif` |
| Hourly Radiation | `radiation_20240115T12.tif` | `RAD_Ed01a_TOA-TS-HR-GLOB-ASWDN_2024011512_RFA01.tif` |

---

## Best Practices

### When to Use VEDA Conventions

✅ **Use VEDA when:**
- Working with GHG Center or VEDA platform
- Simplicity and readability are priorities
- Files are for visualization/exploration
- Working with modern cloud-native workflows
- Need flexible datetime formats

### When to Use NASA ASDC Conventions

✅ **Use NASA ASDC when:**
- Contributing to NASA archives
- Working with GEWEX or similar programs
- Need extensive metadata in filename
- Following established NASA standards
- Working with legacy systems

### General Recommendations

1. **Be Consistent**: Choose one convention and stick to it within a project
2. **Document Your Choice**: Include naming convention in README
3. **Validate Names**: Use regex patterns to validate filenames
4. **Preserve Metadata**: Consider using STAC for additional metadata
5. **Test Ingestion**: Verify files work with target systems

---

## Quick Reference

### VEDA Quick Patterns
```bash
# Basic pattern
dataset_YYYYMMDD.tif

# With version
dataset_v1.0_YYYYMMDD.tif

# With timestamp
dataset_YYYYMMDDTHHMMSSZ.tif

# Range
dataset_YYYYMMDD_YYYYMMDD.tif
```

### NASA ASDC Quick Pattern
```bash
PRODUCT_Version_Category-Type-Interval-Area-Parameter_TimeTag_RFAVersion.ext
```

### Conversion Guide

| From VEDA | To NASA ASDC |
|-----------|--------------|
| `temp_202401.tif` | `TEMP_Ed01a_SFC-MAP-MON-GLOB-TEMP_2024019999_RFA01.tif` |
| `precip_20240115_20240131.tif` | `PRECIP_Ed01a_SFC-MAP-DAY-GLOB-PRCP_2024011599-2024013199_RFA01.tif` |

| From NASA ASDC | To VEDA |
|----------------|---------|
| `NDVI_Ed01a_SFC-MAP-MON-GLOB-NDVI_2024019999_RFA01.tif` | `ndvi_202401.tif` |
| `CH4_Ed02b_TOA-MAP-DAY-GLOB-CH4_2024011512_RFA01.tif` | `ch4_20240115T12.tif` |

---

## Summary

Both VEDA and NASA ASDC file naming conventions serve important purposes:

- **VEDA** prioritizes simplicity, flexibility, and modern cloud workflows
- **NASA ASDC** prioritizes systematic organization, metadata preservation, and archival standards

Choose based on your target system, organizational requirements, and the need for embedded metadata versus external metadata catalogs.

---

## Resources

- [VEDA Platform Documentation](https://docs.openveda.cloud/)
- [NASA ASDC GEWEX Documentation](https://asdc.larc.nasa.gov/documents/gewex-rfa/documents/)
- [STAC Specification](https://stacspec.org/)
- [Cloud Optimized GeoTIFF](https://www.cogeo.org/)
- [Regex Testing Tool](https://regex101.com/)

---

*Last Updated: 2024*