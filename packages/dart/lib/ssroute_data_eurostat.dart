library ssroute_data_eurostat;

export 'src/models.dart';
export 'src/data.dart' show nodesData, edgesData, metaData;

import 'src/data.dart' as embedded_data;
import 'src/models.dart';

/// Loads the nodes as a list of [Node] objects from the package.
///
/// Each node is represented as a tuple [id, lon, lat].
/// Works in all Dart environments (VM, Flutter mobile, Flutter web).
List<Node> loadNodes() {
  final json = embedded_data.nodesData;
  return json.map((item) => Node.fromJson(item as List)).toList();
}

/// Loads the edges as a list of [Edge] objects from the package.
///
/// Each edge is represented as a tuple [from, to, lengthNm].
/// Works in all Dart environments (VM, Flutter mobile, Flutter web).
List<Edge> loadEdges() {
  final json = embedded_data.edgesData;
  return json.map((item) => Edge.fromJson(item as List)).toList();
}

/// Loads the metadata [Meta] object (schema, units, etc.) from the package.
///
/// Works in all Dart environments (VM, Flutter mobile, Flutter web).
Meta loadMeta() {
  final json = embedded_data.metaData;
  return Meta.fromJson(json);
}

