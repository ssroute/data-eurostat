# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-12

### Breaking Changes
- `loadNodes()`, `loadEdges()`, and `loadMeta()` are now **synchronous** (removed `Future` return types)
- Functions now return typed model objects (`List<Node>`, `List<Edge>`, `Meta`) instead of `Map<String, dynamic>` GeoJSON structures
- Data format changed from GeoJSON FeatureCollections to JSON tuple arrays

### Added
- `Node`, `Edge`, and `Meta` model classes with `fromJson`/`toJson` methods
- Raw data exports: `nodesData`, `edgesData`, `metaData` for advanced use cases
- Support for Flutter web (data embedded at build time, no file I/O required)

### Changed
- Data is now embedded directly in the package (no runtime file I/O)
- Works seamlessly across all Dart environments: VM, Flutter mobile, and Flutter web

## [0.1.0] - Initial Release

### Added
- Initial release
- Embedded Eurostat SeaRoute / MARNET maritime routing graph data
- API: `loadNodes()`, `loadEdges()`, `loadMeta()` (async, GeoJSON-based)
