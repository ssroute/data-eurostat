library ssroute_data_eurostat;

import 'dart:convert';
import 'dart:io';
import 'dart:isolate';

Future<Map<String, dynamic>> _loadJson(String packageRelativePath) async {
  // packageRelativePath like 'src/data/nodes.geojson'
  final uri = await Isolate.resolvePackageUri(
    Uri.parse('package:ssroute_data_eurostat/$packageRelativePath'),
  );
  if (uri == null) {
    throw StateError('Could not resolve package URI for $packageRelativePath');
  }
  final file = File.fromUri(uri);
  final contents = await file.readAsString();
  return jsonDecode(contents) as Map<String, dynamic>;
}

/// Loads the nodes GeoJSON FeatureCollection from the package.
Future<Map<String, dynamic>> loadNodes() {
  return _loadJson('src/data/nodes.geojson');
}

/// Loads the edges GeoJSON FeatureCollection from the package.
Future<Map<String, dynamic>> loadEdges() {
  return _loadJson('src/data/edges.geojson');
}

/// Loads the metadata JSON (schema, units, etc.) from the package.
Future<Map<String, dynamic>> loadMeta() {
  return _loadJson('src/data/meta.json');
}

