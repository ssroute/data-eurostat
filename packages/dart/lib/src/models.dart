/// Model classes for Eurostat SeaRoute / MARNET graph data.

/// A node in the graph representing a waypoint on the sea surface.
class Node {
  final int id;
  final double lon;
  final double lat;

  const Node({
    required this.id,
    required this.lon,
    required this.lat,
  });

  /// Creates a Node from a JSON array [id, lon, lat].
  factory Node.fromJson(List<dynamic> json) {
    if (json.length != 3) {
      throw FormatException('Expected [id, lon, lat], got $json');
    }
    return Node(
      id: json[0] as int,
      lon: (json[1] as num).toDouble(),
      lat: (json[2] as num).toDouble(),
    );
  }

  /// Converts this Node to a JSON array [id, lon, lat].
  List<dynamic> toJson() => [id, lon, lat];

  @override
  String toString() => 'Node(id: $id, lon: $lon, lat: $lat)';
}

/// An edge in the graph representing a directed connection between nodes.
class Edge {
  final int from;
  final int to;
  final double lengthNm;

  const Edge({
    required this.from,
    required this.to,
    required this.lengthNm,
  });

  /// Creates an Edge from a JSON array [from, to, lengthNm].
  factory Edge.fromJson(List<dynamic> json) {
    if (json.length != 3) {
      throw FormatException('Expected [from, to, lengthNm], got $json');
    }
    return Edge(
      from: json[0] as int,
      to: json[1] as int,
      lengthNm: (json[2] as num).toDouble(),
    );
  }

  /// Converts this Edge to a JSON array [from, to, lengthNm].
  List<dynamic> toJson() => [from, to, lengthNm];

  @override
  String toString() => 'Edge(from: $from, to: $to, lengthNm: $lengthNm)';
}

/// Metadata describing the graph data schema and units.
class Meta {
  final String distanceUnits;
  final List<String> nodeSchema;
  final List<String> edgeSchema;

  const Meta({
    required this.distanceUnits,
    required this.nodeSchema,
    required this.edgeSchema,
  });

  /// Creates a Meta from a JSON object.
  factory Meta.fromJson(Map<String, dynamic> json) {
    return Meta(
      distanceUnits: json['distance_units'] as String,
      nodeSchema: List<String>.from(json['node_schema'] as List),
      edgeSchema: List<String>.from(json['edge_schema'] as List),
    );
  }

  /// Converts this Meta to a JSON object.
  Map<String, dynamic> toJson() => {
        'distance_units': distanceUnits,
        'node_schema': nodeSchema,
        'edge_schema': edgeSchema,
      };

  @override
  String toString() => 'Meta(distanceUnits: $distanceUnits, nodeSchema: $nodeSchema, edgeSchema: $edgeSchema)';
}
