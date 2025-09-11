# STAC Temporal Intervals Reference

This document provides a comprehensive list of temporal intervals used in STAC (SpatioTemporal Asset Catalog) specifications following ISO 8601 duration format.

## Duration Format

STAC temporal intervals follow the ISO 8601 duration format: `P[n]Y[n]M[n]DT[n]H[n]M[n]S`

Where:
- `P` is the duration designator (for period) placed at the start of the duration representation
- `Y` is the year designator that follows the value for the number of years
- `M` is the month designator that follows the value for the number of months
- `D` is the day designator that follows the value for the number of days
- `T` is the time designator that precedes the time components of the representation
- `H` is the hour designator that follows the value for the number of hours
- `M` is the minute designator that follows the value for the number of minutes
- `S` is the second designator that follows the value for the number of seconds

## Common Temporal Intervals

### Sub-Daily Intervals
- `PT1M` - 1 minute
- `PT5M` - 5 minutes
- `PT10M` - 10 minutes
- `PT15M` - 15 minutes
- `PT30M` - 30 minutes
- `PT1H` - 1 hour
- `PT2H` - 2 hours
- `PT3H` - 3 hours
- `PT4H` - 4 hours
- `PT6H` - 6 hours
- `PT8H` - 8 hours
- `PT12H` - 12 hours

### Daily Intervals
- `P1D` - 1 day (24 hours)
- `P2D` - 2 days
- `P3D` - 3 days
- `P4D` - 4 days
- `P5D` - 5 days
- `P6D` - 6 days

### Weekly Intervals
- `P1W` or `P7D` - 1 week
- `P2W` or `P14D` - 2 weeks

### Monthly Intervals
- `P1M` - 1 month
- `P2M` - 2 months
- `P3M` - 3 months (quarterly)
- `P4M` - 4 months
- `P6M` - 6 months (semi-annual)

### Annual Intervals
- `P1Y` - 1 year
- `P2Y` - 2 years
- `P5Y` - 5 years
- `P10Y` - 10 years

### Combined Intervals
- `P1Y2M` - 1 year and 2 months
- `P1DT12H` - 1 day and 12 hours
- `P1MT6H` - 1 month and 6 hours
- `PT1H30M` - 1 hour and 30 minutes

## Special Cases

### Real-time or Near Real-time
- `PT0S` - Instantaneous/real-time data

### Irregular Intervals
Some datasets may have irregular temporal patterns. In these cases, the temporal extent is specified but not a regular interval.

## Usage in STAC

In STAC collections, temporal intervals are typically specified in the collection metadata under temporal extent properties. For example:

```json
{
  "extent": {
    "temporal": {
      "interval": [["2020-01-01T00:00:00Z", "2023-12-31T23:59:59Z"]]
    }
  },
  "summaries": {
    "temporal_resolution": ["P1D"]
  }
}
```

## Examples by Data Type

### Satellite Imagery
- Landsat: `P16D` (16-day revisit cycle)
- Sentinel-2: `P5D` (5-day revisit cycle at equator)
- MODIS daily: `P1D`
- GOES: `PT10M` or `PT15M` (geostationary weather satellites)

### Climate Data
- Daily aggregates: `P1D`
- Monthly averages: `P1M`
- Seasonal data: `P3M`
- Annual summaries: `P1Y`

### Weather Data
- Radar data: `PT5M` or `PT10M`
- Hourly observations: `PT1H`
- 3-hourly forecasts: `PT3H`
- Daily summaries: `P1D`

## References
- [ISO 8601 Duration Format](https://en.wikipedia.org/wiki/ISO_8601#Durations)
- [STAC Specification](https://github.com/radiantearth/stac-spec)