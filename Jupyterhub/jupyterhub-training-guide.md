# JupyterHub Training Guide - Disasters Hub

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [JupyterHub Interface Overview](#jupyterhub-interface-overview)
4. [Working with Jupyter Notebooks](#working-with-jupyter-notebooks)
5. [Data Management](#data-management)
6. [Environment and Package Management](#environment-and-package-management)
7. [Terminal and Command Line Access](#terminal-and-command-line-access)
8. [Collaboration and Sharing](#collaboration-and-sharing)
9. [Resource Management](#resource-management)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [Keyboard Shortcuts](#keyboard-shortcuts)
13. [Resources and Links](#resources-and-links)

---

## Introduction

### What is JupyterHub?

JupyterHub is a multi-user server that manages and provides web-based Jupyter notebook environments for multiple users. It allows you to:

- **Access powerful computing resources** through your web browser
- **Write and execute code** in Python, R, Julia, and other languages
- **Visualize data** with interactive plots and charts
- **Collaborate** with team members on shared projects
- **Work from anywhere** without local setup requirements

### The Disasters Hub

The **Disasters Hub** (https://hub.disasters.2i2c.cloud/) is a specialized JupyterHub instance designed for disaster response and analysis work. It provides:

- Pre-configured environments for geospatial analysis
- Access to disaster-related datasets
- Collaboration tools for response teams
- Integration with cloud storage services
- Scalable computing resources

### Key Benefits

✅ **No Installation Required** - Everything runs in your browser  
✅ **Pre-configured Environments** - Common packages already installed  
✅ **Persistent Storage** - Your work is saved between sessions  
✅ **Collaboration Ready** - Share notebooks with team members  
✅ **Scalable Resources** - Access to GPU and high-memory instances when needed  

---

## Getting Started

### Accessing the Disasters Hub

1. **Navigate to the Hub**
   - Open your web browser (Chrome, Firefox, Safari, or Edge recommended)
   - Go to: https://hub.disasters.2i2c.cloud/
   - Bookmark this URL for easy access

2. **Authentication**
   - You'll see a login screen with authentication options
   - Common authentication methods:
     - **GitHub**: Use your GitHub credentials
     - **Google**: Use your Google account
     - **Institutional Login**: Use your organization's credentials
   - Select your authentication method and follow the prompts

3. **First-Time Login**
   - Accept terms of service if prompted
   - Your home directory will be created automatically
   - Initial setup may take 30-60 seconds

### Server Selection

After login, you may be presented with server options:

```
Server Options:
┌─────────────────────────────────────┐
│ • Small (2 CPU, 4GB RAM)            │
│ • Medium (4 CPU, 8GB RAM)           │
│ • Large (8 CPU, 16GB RAM)           │
│ • GPU Instance (if available)       │
└─────────────────────────────────────┘
```

**Tips for Server Selection:**
- Start with **Small** for basic notebook work
- Use **Medium** for data processing tasks
- Choose **Large** for machine learning or big data
- Select **GPU** only when needed (limited availability)

---

## JupyterHub Interface Overview

### The JupyterLab Interface

Once logged in, you'll see the JupyterLab interface:

```
┌──────────────────────────────────────────────────────────┐
│ [File] [Edit] [View] [Run] [Kernel] [Tabs] [Settings]   │
├──────────────────────────────────────────────────────────┤
│ 📁 File Browser │          Main Work Area                │
│ ├── 📂 data     │                                        │
│ ├── 📂 notebooks│      [Launcher Tab]                     │
│ ├── 📂 scripts  │      • Notebook (Python 3)              │
│ └── 📄 README   │      • Console                          │
│                 │      • Terminal                          │
│ [+] New         │      • Text File                         │
└──────────────────────────────────────────────────────────┘
```

### Key Interface Components

1. **Top Menu Bar**
   - File operations, editing, running code
   - Kernel management
   - View options and settings

2. **Left Sidebar**
   - **File Browser** (📁): Navigate and manage files
   - **Running Terminals and Kernels** (▶): Monitor active sessions
   - **Command Palette** (🔧): Access all commands
   - **Extension Manager** (🧩): Add functionality

3. **Main Work Area**
   - Multiple tabs for notebooks, terminals, and files
   - Drag tabs to rearrange or create split views
   - Right-click tabs for additional options

4. **Status Bar**
   - Current kernel status
   - Line/column position
   - File encoding and type

### Creating Your First Notebook

1. Click the **Python 3** icon in the Launcher
2. Or: File → New → Notebook
3. Select kernel (usually Python 3)
4. Rename your notebook: Right-click on "Untitled.ipynb" → Rename

---

## Working with Jupyter Notebooks

### Notebook Basics

A Jupyter notebook consists of **cells** that can contain:
- **Code**: Executable Python (or other language) code
- **Markdown**: Formatted text, equations, and images
- **Raw**: Unformatted text

### Cell Operations

#### Running Cells
- **Run current cell**: `Shift + Enter` (run and move to next)
- **Run current cell in place**: `Ctrl + Enter` (stay in cell)
- **Run all cells**: Menu → Run → Run All Cells

#### Cell Types
```python
# Code Cell Example
import pandas as pd
import numpy as np
data = pd.read_csv('data.csv')
data.head()
```

```markdown
# Markdown Cell Example
## Analysis Results
- **Finding 1**: Data shows increasing trend
- **Finding 2**: Correlation coefficient: 0.85

$$E = mc^2$$  # LaTeX equation
```

#### Cell Management
- **Insert cell above**: `A` (in command mode)
- **Insert cell below**: `B` (in command mode)
- **Delete cell**: `DD` (press D twice in command mode)
- **Copy cell**: `C` (in command mode)
- **Paste cell**: `V` (in command mode)
- **Undo deletion**: `Z` (in command mode)

### Working with Kernels

The **kernel** is the computational engine that executes your code.

#### Kernel Operations
- **Restart kernel**: Kernel → Restart
- **Restart and clear output**: Kernel → Restart & Clear Output
- **Restart and run all**: Kernel → Restart & Run All
- **Interrupt execution**: Kernel → Interrupt (or `I,I` in command mode)
- **Change kernel**: Kernel → Change Kernel

#### Kernel Status Indicators
- **○**: Kernel idle
- **●**: Kernel busy
- **[*]**: Cell currently executing
- **[1]**: Cell execution number

### Notebook Best Practices

1. **Use meaningful cell divisions**
   - One concept or operation per cell
   - Separate imports, data loading, processing, visualization

2. **Document your work**
   ```python
   # Good practice: Add comments and markdown cells
   # Load disaster response data
   df = pd.read_csv('disaster_data.csv')
   
   # Data preprocessing
   df['date'] = pd.to_datetime(df['date'])
   df = df.dropna()
   ```

3. **Clear output before sharing**
   - Kernel → Restart & Clear Output
   - Reduces file size and removes sensitive output

---

## Data Management

### File Upload/Download

#### Uploading Files
1. **Drag and drop** files directly into the file browser
2. **Upload button**: Click the ⬆ button in the file browser toolbar
3. **Terminal upload**: Use `wget` or `curl` in terminal
   ```bash
   wget https://example.com/data.csv
   curl -O https://example.com/data.zip
   ```

#### Downloading Files
1. **Right-click** file in browser → Download
2. **From notebook**:
   ```python
   from IPython.display import FileLink
   FileLink('results.csv')  # Creates downloadable link
   ```

### Working with Cloud Storage

#### AWS S3 Integration
```python
import boto3
import pandas as pd

# Read from S3
df = pd.read_csv('s3://bucket-name/path/to/file.csv')

# Write to S3
df.to_csv('s3://bucket-name/output/results.csv', index=False)
```

#### Google Cloud Storage
```python
# Read from GCS
df = pd.read_csv('gs://bucket-name/path/to/file.csv')

# Using gsutil in terminal
!gsutil cp gs://bucket/file.csv ./data/
```

### Data Organization

Recommended directory structure:
```
home/
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned, transformed data
│   └── external/      # Data from external sources
├── notebooks/
│   ├── exploratory/   # Initial explorations
│   ├── analysis/      # Detailed analysis
│   └── reports/       # Final reports
├── scripts/           # Reusable Python scripts
├── results/           # Output files, figures
└── requirements.txt   # Package dependencies
```

### Data Persistence

⚠️ **Important**: Your home directory is persistent, but understand the storage limits:

- **Home directory**: Usually 10-100 GB (persistent)
- **Shared data**: Read-only datasets available to all users
- **Temporary storage**: `/tmp` cleared on restart
- **Best practice**: Store large datasets in cloud storage, not home directory

---

## Environment and Package Management

### Installing Packages

#### Using pip (Python packages)
```python
# In a notebook cell
!pip install package_name

# Install specific version
!pip install pandas==1.3.0

# Install from requirements file
!pip install -r requirements.txt

# Install in user directory (if no write permissions)
!pip install --user package_name
```

#### Using conda
```python
# In a notebook cell
!conda install -c conda-forge package_name -y

# Install multiple packages
!conda install numpy pandas matplotlib -y

# Create new environment
!conda create -n myenv python=3.9 -y
!conda activate myenv  # Note: Activation in notebooks is tricky
```

### Managing Python Environments

#### Check current environment
```python
import sys
print(sys.executable)  # Python interpreter path
print(sys.version)     # Python version

# List installed packages
!pip list
!conda list
```

#### Creating isolated environments
```bash
# In terminal
python -m venv myproject
source myproject/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Using Different Kernels

1. **Install IPython kernel**:
   ```bash
   python -m ipykernel install --user --name mykernel --display-name "My Kernel"
   ```

2. **List available kernels**:
   ```bash
   jupyter kernelspec list
   ```

3. **Remove a kernel**:
   ```bash
   jupyter kernelspec uninstall mykernel
   ```

---

## Terminal and Command Line Access

### Opening Terminal

1. **From Launcher**: Click "Terminal" icon
2. **From menu**: File → New → Terminal
3. **Keyboard shortcut**: (varies by setup)

### Common Terminal Commands

```bash
# Navigation
pwd                     # Print working directory
ls -la                  # List files with details
cd ~/notebooks         # Change directory

# File operations
mkdir project          # Create directory
cp file1.txt file2.txt # Copy file
mv oldname newname     # Move/rename
rm file.txt           # Delete file (careful!)

# File viewing
cat file.txt          # Display file contents
head -n 10 data.csv   # First 10 lines
tail -n 10 log.txt    # Last 10 lines
less large_file.txt   # Page through file

# Process management
ps aux                # List processes
top                   # Monitor resources
kill -9 PID          # Kill process

# Git operations
git status
git add .
git commit -m "message"
git push
```

### Working with Data Files

```bash
# Count lines in file
wc -l data.csv

# View CSV structure
head -1 data.csv | tr ',' '\n' | nl

# Search in files
grep "pattern" file.txt
grep -r "pattern" ./directory

# Compress/decompress
zip archive.zip file1 file2
unzip archive.zip
tar -czf archive.tar.gz directory/
tar -xzf archive.tar.gz
```

---

## Collaboration and Sharing

### Sharing Notebooks

#### Method 1: Direct File Sharing
1. Download notebook: File → Download as → Notebook (.ipynb)
2. Share via email, Slack, or file sharing service
3. Recipient uploads to their JupyterHub

#### Method 2: Using Git
```bash
# Initialize repository
git init
git add notebook.ipynb
git commit -m "Add analysis notebook"
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

#### Method 3: Export Formats
- **HTML**: File → Export Notebook As → HTML
- **PDF**: File → Export Notebook As → PDF (requires LaTeX)
- **Python script**: File → Export Notebook As → Python
- **Markdown**: File → Export Notebook As → Markdown

### Real-time Collaboration

Some JupyterHub deployments support real-time collaboration:

1. **Share workspace link**: Get shareable link from hub admin
2. **Collaborative editing**: Multiple users can edit simultaneously
3. **See collaborator cursors**: Real-time cursor positions
4. **Chat integration**: Built-in chat for discussion

### Version Control Best Practices

1. **Clear outputs before committing**:
   ```bash
   jupyter nbconvert --clear-output notebook.ipynb
   ```

2. **Use .gitignore**:
   ```
   .ipynb_checkpoints/
   __pycache__/
   *.pyc
   .DS_Store
   data/  # Don't commit large data files
   ```

3. **Notebook diff tools**:
   ```bash
   # Install nbdime for better notebook diffs
   pip install nbdime
   nbdime config-git --enable
   ```

---

## Resource Management

### Understanding Resource Limits

Your JupyterHub instance has resource limits:

```python
# Check available resources
import psutil

# Memory
memory = psutil.virtual_memory()
print(f"Total RAM: {memory.total / 1e9:.2f} GB")
print(f"Available: {memory.available / 1e9:.2f} GB")
print(f"Used: {memory.percent}%")

# CPU
print(f"CPU cores: {psutil.cpu_count()}")
print(f"CPU usage: {psutil.cpu_percent()}%")

# Disk
disk = psutil.disk_usage('/')
print(f"Disk space: {disk.total / 1e9:.2f} GB")
print(f"Disk used: {disk.percent}%")
```

### Monitoring Resource Usage

#### JupyterLab Extension
- Install Resource Usage extension
- Shows real-time memory and CPU usage in status bar

#### Command line monitoring
```bash
# Real-time resource monitoring
top
htop  # If installed

# Memory usage
free -h

# Disk usage
df -h
du -sh *  # Directory sizes
```

### Optimizing Resource Usage

1. **Clear variables when done**:
   ```python
   # Clear specific variable
   del large_dataframe
   
   # Clear all variables
   %reset -f
   
   # Garbage collection
   import gc
   gc.collect()
   ```

2. **Use efficient data types**:
   ```python
   # Use categories for strings with few unique values
   df['category'] = df['category'].astype('category')
   
   # Use smaller numeric types when possible
   df['count'] = df['count'].astype('int32')  # Instead of int64
   ```

3. **Process data in chunks**:
   ```python
   # Read large CSV in chunks
   chunk_size = 10000
   for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
       process_chunk(chunk)
   ```

### Shutting Down Properly

Always shut down kernels and terminals when done:

1. **Shutdown kernel**: Kernel → Shutdown
2. **Close terminals**: Exit or `Ctrl+D`
3. **Hub Control Panel**: File → Hub Control Panel → Stop My Server
4. **Logout**: File → Log Out

⚠️ **Important**: Idle servers may be automatically culled after a period of inactivity (usually 1-2 hours).

---

## Best Practices

### Project Organization

1. **Use consistent naming**:
   ```
   2024-01-15_earthquake_analysis.ipynb  # Good
   untitled1.ipynb                       # Bad
   ```

2. **Create project templates**:
   ```python
   # notebook_template.ipynb
   
   # 1. Imports
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   
   # 2. Configuration
   pd.set_option('display.max_columns', None)
   plt.style.use('seaborn')
   
   # 3. Data Loading
   
   # 4. Data Exploration
   
   # 5. Analysis
   
   # 6. Results
   ```

3. **Document dependencies**:
   ```python
   # Generate requirements.txt
   !pip freeze > requirements.txt
   ```

### Security Considerations

1. **Never commit credentials**:
   ```python
   # Bad
   api_key = "sk-abc123def456"
   
   # Good - Use environment variables
   import os
   api_key = os.environ.get('API_KEY')
   ```

2. **Use secrets management**:
   ```python
   # Store secrets in .env file
   from dotenv import load_dotenv
   load_dotenv()
   
   # Access secrets
   secret = os.getenv('SECRET_KEY')
   ```

3. **Be careful with outputs**:
   - Clear cells containing sensitive information
   - Review notebooks before sharing

### Performance Tips

1. **Vectorize operations**:
   ```python
   # Slow
   results = []
   for i in range(len(df)):
       results.append(df.iloc[i]['column'] * 2)
   
   # Fast
   results = df['column'] * 2
   ```

2. **Use built-in functions**:
   ```python
   # Use pandas/numpy operations instead of loops
   df['new_col'] = df['col1'] + df['col2']  # Vectorized
   ```

3. **Profile your code**:
   ```python
   %%time  # Time entire cell
   
   %timeit function()  # Time single line
   
   # Detailed profiling
   %load_ext line_profiler
   %lprun -f function_to_profile function_to_profile()
   ```

---

## Troubleshooting

### Common Issues and Solutions

#### Kernel Won't Start
- **Check resources**: Server might be full
- **Try different kernel**: Some kernels may be broken
- **Restart server**: Hub Control Panel → Stop → Start

#### Package Import Errors
```python
# Check if package is installed
import importlib
if importlib.util.find_spec("package_name") is None:
    !pip install package_name
    
# Restart kernel after installation
from IPython import get_ipython
get_ipython().kernel.do_shutdown(True)
```

#### Out of Memory Errors
1. Clear unnecessary variables: `del variable_name`
2. Use smaller data samples for testing
3. Request larger server instance
4. Process data in chunks

#### Notebook Won't Save
- **Check disk space**: `df -h` in terminal
- **Check file permissions**: `ls -la notebook.ipynb`
- **Save with new name**: File → Save As
- **Download backup**: File → Download

#### Connection Issues
- **Check internet connection**
- **Try different browser**
- **Clear browser cache**
- **Check if hub is under maintenance**

### Getting Help

1. **Built-in help**:
   ```python
   help(function_name)
   function_name?  # Quick help
   function_name??  # Source code
   ```

2. **Documentation**:
   - JupyterHub docs: https://jupyterhub.readthedocs.io
   - JupyterLab docs: https://jupyterlab.readthedocs.io
   - 2i2c docs: https://docs.2i2c.org

3. **Community support**:
   - Discourse forum
   - GitHub issues
   - Stack Overflow with tags: `jupyter`, `jupyterhub`

---

## Keyboard Shortcuts

### Command Mode (Blue cell border)
Press `Esc` to enter command mode

| Shortcut | Action |
|----------|--------|
| `Enter` | Enter edit mode |
| `A` | Insert cell above |
| `B` | Insert cell below |
| `D,D` | Delete cell |
| `Y` | Change to code cell |
| `M` | Change to markdown cell |
| `Shift+Up/Down` | Select multiple cells |
| `Shift+M` | Merge selected cells |
| `C` | Copy cell |
| `X` | Cut cell |
| `V` | Paste cell below |
| `Shift+V` | Paste cell above |
| `Z` | Undo cell deletion |
| `0,0` | Restart kernel |
| `I,I` | Interrupt kernel |

### Edit Mode (Green cell border)
Press `Enter` to enter edit mode

| Shortcut | Action |
|----------|--------|
| `Esc` | Enter command mode |
| `Ctrl+Enter` | Run cell |
| `Shift+Enter` | Run cell, select below |
| `Alt+Enter` | Run cell, insert below |
| `Ctrl+S` | Save notebook |
| `Tab` | Code completion |
| `Shift+Tab` | Tooltip |
| `Ctrl+]` | Indent |
| `Ctrl+[` | Dedent |
| `Ctrl+A` | Select all |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

### JupyterLab Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+C` | Command palette |
| `Ctrl+B` | Toggle left sidebar |
| `Ctrl+Shift+D` | Toggle file browser |
| `Ctrl+Shift+F` | Find and replace |
| `Ctrl+Shift+[` | Previous tab |
| `Ctrl+Shift+]` | Next tab |
| `Alt+W` | Close tab |

---

## Resources and Links

### Official Documentation

- **JupyterHub Documentation**: https://jupyterhub.readthedocs.io
- **JupyterLab Documentation**: https://jupyterlab.readthedocs.io
- **Jupyter Notebook Documentation**: https://jupyter-notebook.readthedocs.io
- **2i2c Infrastructure Guide**: https://docs.2i2c.org

### Tutorials and Learning Resources

- **Jupyter Tutorial**: https://jupyter.org/try
- **Real Python Jupyter Guide**: https://realpython.com/jupyter-notebook-introduction/
- **DataCamp Jupyter Tutorial**: https://www.datacamp.com/tutorial/tutorial-jupyter-notebook
- **Official Jupyter Examples**: https://github.com/jupyter/jupyter/wiki/Gallery-of-Jupyter-Notebooks

### Disaster Response Specific Resources

- **NASA Disasters Program**: https://disasters.nasa.gov
- **USGS Hazards Data**: https://www.usgs.gov/natural-hazards
- **NOAA Disaster Data**: https://www.ncdc.noaa.gov/billions/
- **Copernicus Emergency Management**: https://emergency.copernicus.eu

### Python Libraries for Disaster Analysis

```python
# Geospatial analysis
import geopandas as gpd
import rasterio
import xarray as xr
import folium

# Data processing
import pandas as pd
import numpy as np
import dask.dataframe as dd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Machine learning
from sklearn import *
import tensorflow as tf
import torch

# Earth observation
import ee  # Google Earth Engine
import planetary_computer as pc
import pystac_client
```

### Helpful Extensions

Install JupyterLab extensions for enhanced functionality:

```bash
# Variable inspector
jupyter labextension install @lckr/jupyterlab_variableinspector

# Table of contents
jupyter labextension install @jupyterlab/toc

# Git integration
pip install jupyterlab-git

# Code formatter
pip install jupyterlab-code-formatter
```

### Community and Support

- **Jupyter Discourse Forum**: https://discourse.jupyter.org
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/jupyter
- **GitHub Issues**: https://github.com/jupyterhub/jupyterhub/issues
- **2i2c Support**: https://2i2c.org/support
- **Gitter Chat**: https://gitter.im/jupyterhub/jupyterhub

### Quick Reference PDFs

- **JupyterLab Cheat Sheet**: https://www.datacamp.com/cheat-sheet/jupyterlab-cheat-sheet
- **Jupyter Shortcuts PDF**: https://www.cheatography.com/weidadeyue/cheat-sheets/jupyter-notebook/
- **Markdown Guide**: https://www.markdownguide.org/cheat-sheet/

---

## Appendix: Sample Workflow

Here's a complete example workflow for disaster analysis:

```python
# 1. Setup and Imports
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 2. Load Data
# Earthquake data
earthquakes = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv')
earthquakes['time'] = pd.to_datetime(earthquakes['time'])

# 3. Data Processing
# Filter recent events
recent = earthquakes[earthquakes['time'] > datetime.now() - timedelta(days=7)]

# Convert to GeoDataFrame
geometry = gpd.points_from_xy(recent.longitude, recent.latitude)
geo_df = gpd.GeoDataFrame(recent, geometry=geometry, crs='EPSG:4326')

# 4. Analysis
print(f"Total earthquakes in last 7 days: {len(recent)}")
print(f"Average magnitude: {recent['mag'].mean():.2f}")
print(f"Largest earthquake: {recent['mag'].max():.2f}")

# 5. Visualization
# Static plot
fig, ax = plt.subplots(figsize=(12, 8))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax, color='lightgray', edgecolor='black')
geo_df.plot(ax=ax, color='red', markersize=geo_df['mag']**2, alpha=0.6)
plt.title('Recent Earthquakes (M4.5+)')
plt.show()

# Interactive map
m = folium.Map(location=[0, 0], zoom_start=2)
for idx, row in geo_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag']*2,
        popup=f"M{row['mag']} - {row['place']}",
        color='red',
        fill=True
    ).add_to(m)
m.save('earthquake_map.html')

# 6. Export Results
geo_df.to_csv('processed_earthquakes.csv', index=False)
print("Analysis complete! Results saved.")
```

---

*Last Updated: 2024*  
*Version: 1.0*  
*Disasters Hub Training Guide*

For additional assistance, contact your hub administrator or visit the 2i2c support portal.