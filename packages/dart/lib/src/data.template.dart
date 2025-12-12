import 'dart:convert';

// NOTE: This is a template file used by scripts/release.py to generate
// packages/dart/lib/src/data.dart with embedded JSON data.
//
// Do not import this file from the package public API.

const String _nodesJson = r'''__NODES_JSON_PLACEHOLDER__''';
const String _edgesJson = r'''__EDGES_JSON_PLACEHOLDER__''';
const String _metaJson = r'''__META_JSON_PLACEHOLDER__''';

List<dynamic>? _nodesData;
List<dynamic>? _edgesData;
Map<String, dynamic>? _metaData;

/// Gets the parsed nodes data.
List<dynamic> get nodesData {
  _nodesData ??= jsonDecode(_nodesJson) as List<dynamic>;
  return _nodesData!;
}

/// Gets the parsed edges data.
List<dynamic> get edgesData {
  _edgesData ??= jsonDecode(_edgesJson) as List<dynamic>;
  return _edgesData!;
}

/// Gets the parsed meta data.
Map<String, dynamic> get metaData {
  _metaData ??= jsonDecode(_metaJson) as Map<String, dynamic>;
  return _metaData!;
}


