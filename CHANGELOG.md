# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-12-12

### Added
- Processing dependency: `geopy` (used for high-accuracy geodesic distances on WGS84)

### Changed
- Recomputed edge `length_nm` values using ellipsoidal geodesic distance (WGS84) for improved accuracy (previously Haversine / spherical)

## [0.2.0] - 2025-12-12

### Changed
- Dataset representation switched from GeoJSON FeatureCollections to compact JSON tuple arrays (`nodes.json`, `edges.json`)
- Documentation updated in root `README.md` to explain tuple schema and usage patterns
- Release tooling (`scripts/release.py`) enhanced to automatically sync data and versions into language-specific packages

### Removed
- GeoJSON exports (`nodes.geojson`, `edges.geojson`) - replaced by tuple-based JSON format

## [0.1.0] - Initial Release

### Added
- Initial public dataset release
- Eurostat SeaRoute / MARNET maritime routing graph data in GeoJSON format
- Nodes and edges as GeoJSON FeatureCollections
- Metadata file describing schema and units
- Language packages for JavaScript/TypeScript and Dart


