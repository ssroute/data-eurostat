# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-12

### Breaking Changes
- Data format changed from GeoJSON FeatureCollections to JSON tuple arrays
- `getNodes()`, `getEdges()`, and `getMeta()` now return tuple arrays instead of GeoJSON structures

### Added
- TypeScript type definitions: `Node`, `Edge`, and `Meta` types
- Raw data exports: `nodesData`, `edgesData`, `metaData` for advanced use cases (custom bundling, tree-shaking)
- TypeScript build configuration (`tsconfig.json`)
- TypeScript source entrypoint (`index.ts`) with full type support

### Changed
- Build system migrated from CommonJS to TypeScript compilation (`index.ts` → `dist/`)
- Removed CommonJS entrypoint (`index.cjs`)
- Package now uses TypeScript for both development and distribution
- Data is embedded at build time (works in both browser and Node.js without file I/O)

## [0.1.0] - Initial Release

### Added
- Initial release
- Eurostat SeaRoute / MARNET maritime routing graph data
- CommonJS entrypoint (`index.cjs`)
- API: `getNodes()`, `getEdges()`, `getMeta()` (GeoJSON-based)
- Support for both browser and Node.js environments

