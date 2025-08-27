#!/usr/bin/env python3
"""Check TIFF compression settings to diagnose GDAL predictor issues."""

import sys
from osgeo import gdal

def check_tiff(filepath):
    """Check TIFF file compression and predictor settings."""
    print(f"\nChecking: {filepath}")
    print("-" * 50)
    
    # Open the dataset
    ds = gdal.Open(filepath)
    if not ds:
        print(f"Error: Could not open {filepath}")
        return
    
    # Get basic info
    print(f"Driver: {ds.GetDriver().ShortName}/{ds.GetDriver().LongName}")
    print(f"Size: {ds.RasterXSize} x {ds.RasterYSize} x {ds.RasterCount}")
    
    # Check each band
    for i in range(1, ds.RasterCount + 1):
        band = ds.GetRasterBand(i)
        print(f"\nBand {i}:")
        print(f"  Data Type: {gdal.GetDataTypeName(band.DataType)}")
        print(f"  Block Size: {band.GetBlockSize()}")
        
    # Get metadata and check for compression info
    metadata = ds.GetMetadata("IMAGE_STRUCTURE")
    if metadata:
        print("\nImage Structure Metadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    
    # Try to get TIFF tags directly
    print("\nTIFF Tags (if accessible):")
    try:
        # Common TIFF compression-related tags
        tags = ds.GetMetadata("TIFF")
        if tags:
            for key, value in tags.items():
                print(f"  {key}: {value}")
    except:
        print("  Could not read TIFF tags directly")
    
    ds = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_tiff_compression.py <tiff_file>")
        print("\nThis script checks TIFF compression settings that may cause")
        print("GDAL errors with 64-bit samples and predictor compression.")
        sys.exit(1)
    
    check_tiff(sys.argv[1])