# VEDA Data Visualization Training Guide

## Table of Contents
1. [Introduction to VEDA](#introduction-to-veda)
2. [Getting Started](#getting-started)
3. [Core Concepts](#core-concepts)
4. [MDX Pages and Data Stories](#mdx-pages-and-data-stories)
5. [Dataset Configuration](#dataset-configuration)
6. [Visualization Components](#visualization-components)
7. [Color Schemes and Styling](#color-schemes-and-styling)
8. [Map Visualizations](#map-visualizations)
9. [Best Practices](#best-practices)
10. [Advanced Topics](#advanced-topics)
11. [Resources and References](#resources-and-references)

---

## Introduction to VEDA

VEDA (Visualization, Exploration, and Data Analysis) is NASA's open-source platform for exploring geospatial data through interactive visualizations. It provides a powerful framework for creating data dashboards that combine map layers, time series data, and narrative content.

### Key Features
- **Geospatial Data Visualization**: Display raster and vector data on interactive maps
- **Time Series Analysis**: Explore temporal patterns in environmental data
- **Data Stories**: Create narrative-driven explorations of complex datasets
- **Customizable Dashboards**: Build tailored interfaces for specific research needs

### Architecture Overview
- **Frontend**: [VEDA UI](https://github.com/NASA-IMPACT/veda-ui) - TypeScript-based React application
- **Configuration**: [VEDA Config](https://github.com/NASA-IMPACT/veda-config) - MDX-based content management
- **Data Format**: STAC (SpatioTemporal Asset Catalog) compliant

---

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Git
- Basic understanding of React and MDX
- Familiarity with geospatial concepts

### Installation

1. **Clone the repositories:**
```bash
# Clone the UI repository
git clone https://github.com/NASA-IMPACT/veda-ui.git

# Clone the configuration repository
git clone https://github.com/NASA-IMPACT/veda-config.git
```

2. **Set up environment variables:**
```bash
cp .env.local-sample .env.local
# Edit .env.local with your configuration
```

3. **Install dependencies and run:**
```bash
npm install
npm run dev
```

### Documentation Resources
- [Setup Guide](https://github.com/NASA-IMPACT/veda-config/blob/develop/docs/SETUP.md)
- [GitHub Codespaces Setup](https://github.com/NASA-IMPACT/veda-config/blob/develop/docs/GH_CODESPACES.md)
- [Development Guide](https://github.com/NASA-IMPACT/veda-config/blob/develop/docs/DEVELOPMENT.md)

---

## Core Concepts

### 1. Content Types

VEDA organizes content into two primary types:

#### Datasets
- Geo-referenced data displayed as map layers
- Configured through `.data.mdx` files
- Support for raster and vector formats
- Time-series capable

#### Data Stories
- Long-form narrative content
- Combine text, visualizations, and interactive elements
- Configured through `.stories.mdx` files
- Perfect for explaining complex phenomena

### 2. Configuration Structure

```
veda-config/
├── datasets/           # Dataset configurations
│   ├── co2.data.mdx
│   └── ...
├── stories/           # Data story configurations
│   ├── air-quality-and-covid-19.stories.mdx
│   └── ...
├── custom-pages/      # Custom page layouts
└── admin/            
    └── config.yml     # Global configuration
```

### 3. STAC Integration
VEDA uses STAC specifications for cataloging spatial-temporal assets:
- Standardized metadata
- Efficient data discovery
- Interoperability with other platforms

---

## MDX Pages and Data Stories

### MDX Basics

MDX combines Markdown with JSX, allowing you to embed React components in your content:

```mdx
# My Data Story

import { Map, Chart } from '@veda/components';

This is regular markdown text.

<Map
  layers={['temperature-anomaly']}
  center={[0, 0]}
  zoom={3}
/>

## Analysis Section

<Chart
  data={temperatureData}
  type="line"
/>
```

### Creating a Data Story

1. **Create a new `.stories.mdx` file:**
```mdx
---
id: my-climate-story
name: Climate Change Impacts
description: Exploring temperature anomalies
pubDate: 2024-01-15
media:
  src: ./media/hero-image.jpg
  alt: Climate visualization
---

# Introduction

Your narrative content here...

## Interactive Visualization

<CompareImage
  leftLayer="temperature-2020"
  rightLayer="temperature-2024"
/>
```

### Available Story Examples
- `air-quality-and-covid-19.stories.mdx` - Pandemic air quality changes
- `hurricane-ian.stories.mdx` - Hurricane impact analysis
- `sea-ice-thickness.stories.mdx` - Arctic ice monitoring
- `urban-heating.stories.mdx` - Urban heat island effects
- `tornadoes2024.stories.mdx` - Severe weather tracking

---

## Dataset Configuration

### Basic Dataset Structure

Create a `.data.mdx` file in the `datasets/` directory:

```mdx
---
id: temperature-anomaly
name: Global Temperature Anomaly
description: Monthly temperature deviation from baseline
taxonomy:
  - name: Climate
    values:
      - Temperature
layers:
  - id: temp-anomaly-layer
    stacCol: temperature-collection
    name: Temperature Anomaly
    type: raster
    description: Temperature difference from 1951-1980 average
    zoomExtent: [0, 20]
    sourceParams:
      colormap_name: rdbu
      rescale: [-5, 5]
---

# Dataset Documentation

Additional information about the dataset...
```

### Layer Configuration Options

```yaml
layers:
  - id: unique-layer-id
    name: Display Name
    type: raster | vector
    description: Layer description
    
    # Visualization settings
    zoomExtent: [minZoom, maxZoom]
    initialDatetime: "2024-01-01"
    
    # Source parameters
    sourceParams:
      colormap_name: viridis  # Color scheme
      rescale: [min, max]     # Value range
      nodata: -9999          # No data value
      
    # Legend configuration
    legend:
      type: gradient | categorical
      stops:
        - "#0000ff"  # Blue for low values
        - "#ffffff"  # White for mid values
        - "#ff0000"  # Red for high values
```

---

## Visualization Components

### Map Components

#### Basic Map
```jsx
<Map
  layers={['layer-id']}
  center={[latitude, longitude]}
  zoom={10}
  projection="mercator"
/>
```

#### Layer Comparison
```jsx
<CompareImage
  leftLayer={{
    id: 'before-event',
    datetime: '2023-01-01'
  }}
  rightLayer={{
    id: 'after-event',
    datetime: '2023-12-31'
  }}
/>
```

### Chart Components

#### Time Series Chart
```jsx
<TimeSeriesChart
  datasetId="temperature-anomaly"
  coordinates={[40.7128, -74.0060]}
  dateRange={['2020-01-01', '2024-01-01']}
/>
```

#### Statistical Charts
```jsx
<Chart
  type="bar | line | scatter | histogram"
  data={dataArray}
  options={{
    title: "Chart Title",
    xAxis: { label: "X Label" },
    yAxis: { label: "Y Label" }
  }}
/>
```

### Interactive Elements

#### Layer Switcher
```jsx
<LayerSwitcher
  layers={[
    { id: 'layer-1', name: 'Option 1' },
    { id: 'layer-2', name: 'Option 2' }
  ]}
  defaultLayer="layer-1"
/>
```

#### Date Picker
```jsx
<DatePicker
  start="2020-01-01"
  end="2024-12-31"
  onChange={(date) => handleDateChange(date)}
/>
```

---

## Color Schemes and Styling

### Available Colormaps

VEDA supports over 200 colormaps for data visualization. Common options include:

#### Scientific Colormaps
- `viridis` - Perceptually uniform, colorblind-friendly
- `plasma` - Purple to yellow gradient
- `inferno` - Black to yellow through red
- `magma` - Black to white through purple

#### Diverging Colormaps (for anomalies)
- `rdbu` - Red to blue (via white)
- `coolwarm` - Cool to warm colors
- `seismic` - Blue to red (symmetric)

#### Sequential Colormaps
- `blues` - Light to dark blue
- `greens` - Light to dark green
- `oranges` - Light to dark orange

### Custom Color Configuration

Reference: [admin/config.yml](https://github.com/NASA-IMPACT/veda-config/blob/develop/admin/config.yml)

```yaml
# In layer configuration
sourceParams:
  colormap_name: custom_colormap
  color_formula: |
    colorInterpolate(
      [0, 0.5, 1],
      ['#0000ff', '#ffffff', '#ff0000']
    )
```

### Theme Customization

```javascript
// veda.config.js
export default {
  theme: {
    colors: {
      primary: '#1c5bde',
      secondary: '#f0c000',
      danger: '#c21e56',
      success: '#2ca58d'
    },
    typography: {
      fontFamily: 'Inter, sans-serif',
      fontSize: {
        base: '16px',
        large: '20px'
      }
    }
  }
};
```

---

## Map Visualizations

### Projection Options

VEDA supports multiple map projections for different use cases:

#### Global Projections
```javascript
{
  projection: 'mercator',      // Standard web mapping
  projection: 'naturalEarth',   // Aesthetic world maps
  projection: 'globe',          // 3D globe view
}
```

#### Regional Projections
```javascript
{
  projection: 'albers',         // Continental US
  center: [-96, 39],
  parallels: [29.5, 45.5]
}
```

#### Polar Projections
```javascript
{
  projection: 'polarNorth',     // Arctic view
  projection: 'polarSouth',     // Antarctic view
}
```

### Advanced Map Features

#### Custom Basemaps
```javascript
{
  basemap: {
    url: 'https://tiles.example.com/{z}/{x}/{y}.png',
    attribution: 'Map data © Provider',
    maxZoom: 18
  }
}
```

#### Layer Interactions
```javascript
{
  layers: [{
    id: 'interactive-layer',
    onClick: (feature) => {
      // Handle click events
      console.log(feature.properties);
    },
    onHover: (feature) => {
      // Handle hover events
      showTooltip(feature);
    }
  }]
}
```

---

## Best Practices

### 1. Performance Optimization

#### Tile Caching
- Use Cloud Optimized GeoTIFFs (COGs)
- Implement appropriate zoom constraints
- Leverage browser caching headers

#### Data Loading
```javascript
// Lazy load heavy datasets
const HeavyVisualization = lazy(() => import('./HeavyViz'));

// Use suspense for loading states
<Suspense fallback={<LoadingSpinner />}>
  <HeavyVisualization />
</Suspense>
```

### 2. Accessibility

#### Color Considerations
- Use colorblind-friendly palettes (viridis, cividis)
- Provide alternative data representations
- Include proper contrast ratios

#### Semantic Markup
```mdx
<figure role="img" aria-label="Temperature anomaly map">
  <Map {...props} />
  <figcaption>
    Global temperature anomaly for January 2024
  </figcaption>
</figure>
```

### 3. Responsive Design

```css
/* Mobile-first approach */
.visualization-container {
  width: 100%;
  height: 400px;
}

@media (min-width: 768px) {
  .visualization-container {
    height: 600px;
  }
}
```

### 4. Data Story Guidelines

#### Structure
1. **Hook**: Engaging introduction
2. **Context**: Background information
3. **Exploration**: Interactive visualizations
4. **Insights**: Key findings
5. **Call to Action**: Next steps

#### Writing Tips
- Use clear, concise language
- Define technical terms
- Provide context for data
- Include uncertainty information

---

## Advanced Topics

### 1. Custom Components

Create reusable visualization components:

```jsx
// components/CustomVisualization.jsx
import React from 'react';
import { useDataset } from '@veda/hooks';

export const CustomVisualization = ({ datasetId }) => {
  const { data, loading, error } = useDataset(datasetId);
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  
  return (
    <div className="custom-viz">
      {/* Your visualization logic */}
    </div>
  );
};
```

### 2. Data Processing

#### Client-side Processing
```javascript
// Transform data before visualization
const processedData = rawData.map(point => ({
  ...point,
  value: point.value * conversionFactor,
  timestamp: new Date(point.datetime)
}));
```

#### Server-side Integration
```javascript
// Fetch processed data from API
const fetchProcessedData = async (params) => {
  const response = await fetch('/api/process', {
    method: 'POST',
    body: JSON.stringify(params)
  });
  return response.json();
};
```

### 3. Animation and Transitions

#### Time-lapse Animations
```jsx
<TimelapsePlayer
  layers={monthlyLayers}
  interval={1000}  // milliseconds between frames
  loop={true}
/>
```

#### Smooth Transitions
```css
.layer-transition {
  transition: opacity 0.3s ease-in-out;
}
```

### 4. Integration with External Services

#### STAC API Integration
```javascript
const stacClient = new StacClient({
  url: 'https://stac-api.example.com'
});

const collections = await stacClient.getCollections();
const items = await stacClient.searchItems({
  bbox: [-180, -90, 180, 90],
  datetime: '2024-01-01/2024-12-31'
});
```

### 5. Custom Projections

```javascript
// Define custom projection
import { geoProjection } from 'd3-geo';

const customProjection = geoProjection((x, y) => {
  // Custom projection logic
  return [transformedX, transformedY];
});

// Use in map configuration
{
  projection: customProjection,
  projectionConfig: {
    scale: 150,
    center: [0, 0]
  }
}
```

---

## Resources and References

### Official Documentation
- [VEDA UI Repository](https://github.com/NASA-IMPACT/veda-ui)
- [VEDA Config Repository](https://github.com/NASA-IMPACT/veda-config)
- [VEDA Config Admin Settings](https://github.com/NASA-IMPACT/veda-config/blob/develop/admin/config.yml)

### Related Technologies
- [STAC Specification](https://stacspec.org/)
- [MDX Documentation](https://mdxjs.com/)
- [React Documentation](https://react.dev/)
- [D3.js for Data Visualization](https://d3js.org/)
- [MapLibre GL JS](https://maplibre.org/)

### Learning Resources
- [NASA Earthdata](https://earthdata.nasa.gov/)
- [Cloud Optimized GeoTIFF Guide](https://www.cogeo.org/)
- [Web Mapping Tutorials](https://leafletjs.com/examples.html)

### Community and Support
- [GitHub Issues - VEDA UI](https://github.com/NASA-IMPACT/veda-ui/issues)
- [GitHub Issues - VEDA Config](https://github.com/NASA-IMPACT/veda-config/issues)
- [NASA IMPACT](https://impact.earthdata.nasa.gov/)

### Example Implementations
Review these story files for practical examples:
- Climate Analysis: `air-quality-and-covid-19.stories.mdx`
- Natural Disasters: `hurricane-ian.stories.mdx`, `lahaina-fire.stories.mdx`
- Environmental Monitoring: `sea-ice-thickness.stories.mdx`, `phytoplankton-algal-blooms.stories.mdx`
- Urban Studies: `urban-heating.stories.mdx`
- Extreme Weather: `tornadoes2024.stories.mdx`, `blizzards.stories.mdx`

### Advanced Examples
Explore these for complex visualization patterns:
- Multi-temporal Analysis: `changing-landscapes.stories.mdx`
- Model Comparisons: `CMIP-winter-median-precip-temp.data.mdx`
- Real-time Data: `ercot.stories.mdx` (Texas power grid)
- Water Resources: `tws-trends.stories.mdx`, `wetland-stories.stories.mdx`

---

## Appendix: Quick Reference

### Common Patterns

#### Loading Data
```javascript
import { useEffect, useState } from 'react';

const useVEDAData = (datasetId) => {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch(`/api/datasets/${datasetId}`)
      .then(res => res.json())
      .then(setData);
  }, [datasetId]);
  
  return data;
};
```

#### Error Handling
```javascript
try {
  const result = await fetchVisualizationData();
  renderVisualization(result);
} catch (error) {
  console.error('Visualization error:', error);
  showErrorMessage('Unable to load visualization');
}
```

#### Responsive Maps
```javascript
const MapContainer = () => {
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight * 0.6
  });
  
  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight * 0.6
      });
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return <Map {...dimensions} />;
};
```

---

*This training guide is a living document. For the most up-to-date information, always refer to the official VEDA repositories and documentation.*