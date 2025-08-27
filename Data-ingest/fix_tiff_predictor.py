#!/usr/bin/env python3
"""
Fix TIFF files with predictor compression issues for 64-bit samples.
This script recompresses TIFFs without the predictor to make them GDAL-compatible.
"""

import os
import sys
from osgeo import gdal
import argparse

def fix_tiff_predictor(input_file, output_file=None, compression='DEFLATE'):
    """
    Recompress a TIFF file without predictor to fix GDAL compatibility issues.
    
    Args:
        input_file: Path to input TIFF with predictor issues
        output_file: Path for output TIFF (if None, adds '_fixed' suffix)
        compression: Compression type (NONE, LZW, DEFLATE, ZSTD)
    """
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_fixed{ext}"
    
    print(f"Processing: {input_file}")
    print(f"Output: {output_file}")
    
    # Open source dataset
    src_ds = gdal.Open(input_file)
    if not src_ds:
        print(f"Error: Could not open {input_file}")
        return False
    
    # Create output with specific creation options
    driver = gdal.GetDriverByName('GTiff')
    
    # Creation options to avoid predictor with 64-bit data
    creation_options = [
        f'COMPRESS={compression}',
        'PREDICTOR=1',  # Explicitly set to NONE (1) instead of horizontal differencing (2)
        'TILED=YES',
        'BLOCKXSIZE=512',
        'BLOCKYSIZE=512',
        'BIGTIFF=YES'  # Use BigTIFF for large files
    ]
    
    # Additional options for better compatibility
    if compression == 'DEFLATE':
        creation_options.append('ZLEVEL=6')
    
    print(f"Creation options: {creation_options}")
    
    # Create output dataset
    out_ds = driver.CreateCopy(
        output_file,
        src_ds,
        options=creation_options,
        callback=gdal.TermProgress_nocb
    )
    
    if not out_ds:
        print(f"Error: Could not create {output_file}")
        src_ds = None
        return False
    
    # Flush cache
    out_ds.FlushCache()
    
    # Clean up
    src_ds = None
    out_ds = None
    
    print(f"Successfully created: {output_file}")
    
    # Verify the output can be read
    test_ds = gdal.Open(output_file)
    if test_ds:
        band = test_ds.GetRasterBand(1)
        try:
            # Try to read a small portion to verify it works
            data = band.ReadAsArray(0, 0, min(100, band.XSize), min(100, band.YSize))
            print("Verification: Output file is readable")
            test_ds = None
            return True
        except Exception as e:
            print(f"Warning: Output file created but may still have issues: {e}")
            test_ds = None
            return False
    else:
        print("Error: Could not verify output file")
        return False

def process_directory(directory, pattern="*.tif", compression='DEFLATE'):
    """Process all TIFF files in a directory."""
    import glob
    
    tiff_files = glob.glob(os.path.join(directory, pattern))
    print(f"Found {len(tiff_files)} TIFF files to process")
    
    success_count = 0
    for tiff_file in tiff_files:
        if fix_tiff_predictor(tiff_file, compression=compression):
            success_count += 1
        print("-" * 50)
    
    print(f"\nProcessed {success_count}/{len(tiff_files)} files successfully")

def main():
    parser = argparse.ArgumentParser(
        description='Fix TIFF files with predictor compression issues for 64-bit samples'
    )
    parser.add_argument('input', help='Input TIFF file or directory')
    parser.add_argument(
        '-o', '--output',
        help='Output TIFF file (for single file mode)',
        default=None
    )
    parser.add_argument(
        '-c', '--compression',
        choices=['NONE', 'LZW', 'DEFLATE', 'ZSTD'],
        default='DEFLATE',
        help='Compression type for output (default: DEFLATE)'
    )
    parser.add_argument(
        '-d', '--directory',
        action='store_true',
        help='Process all TIFF files in the input directory'
    )
    parser.add_argument(
        '-p', '--pattern',
        default='*.tif',
        help='File pattern for directory mode (default: *.tif)'
    )
    
    args = parser.parse_args()
    
    # Configure GDAL
    gdal.UseExceptions()
    gdal.SetConfigOption('GDAL_DISABLE_READDIR_ON_OPEN', 'TRUE')
    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
    
    if args.directory:
        if not os.path.isdir(args.input):
            print(f"Error: {args.input} is not a directory")
            sys.exit(1)
        process_directory(args.input, args.pattern, args.compression)
    else:
        if not os.path.isfile(args.input):
            print(f"Error: {args.input} is not a file")
            sys.exit(1)
        success = fix_tiff_predictor(args.input, args.output, args.compression)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()