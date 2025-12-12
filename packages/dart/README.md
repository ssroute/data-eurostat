# ssroute_data_eurostat

Eurostat SeaRoute / MARNET maritime routing graph data (JSON tuples) for Dart.

**Works in all Dart environments** - VM, Flutter mobile, and Flutter web. Data is embedded at build time, no file I/O required.

For a plain-language explanation of the dataset (ELI5), data structure, and how it can be used with Dijkstra/A* for *visualizations* (not navigation), see the main repository README:

- `https://github.com/ssroute/data-eurostat#explain-it-like-im-5`

## Usage

### Dart VM / CLI

```dart
import 'package:ssroute_data_eurostat/ssroute_data_eurostat.dart';

void main() {
  final nodes = loadNodes();
  final edges = loadEdges();
  final meta = loadMeta();

  print('Loaded ${nodes.length} nodes');
  print('Loaded ${edges.length} edges');
  print('Distance units: ${meta.distanceUnits}');
  
  // Access node properties
  final firstNode = nodes.first;
  print('First node: id=${firstNode.id}, lon=${firstNode.lon}, lat=${firstNode.lat}');
  
  // Access edge properties
  final firstEdge = edges.first;
  print('First edge: from=${firstEdge.from}, to=${firstEdge.to}, length=${firstEdge.lengthNm}nm');
}
```

### Flutter (Mobile & Web)

```dart
import 'package:ssroute_data_eurostat/ssroute_data_eurostat.dart';

class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final nodes = loadNodes();
    final edges = loadEdges();
    
    return Text('Loaded ${nodes.length} nodes, ${edges.length} edges');
  }
}
```

### Advanced: Direct Data Access

For custom use cases or tree-shaking:

```dart
import 'package:ssroute_data_eurostat/ssroute_data_eurostat.dart';

void main() {
  // Access raw parsed JSON data
  final rawNodes = nodesData;
  final rawEdges = edgesData;
  final rawMeta = metaData;
}
```

## API

- `List<Node> loadNodes()` - Returns a list of [Node] objects (parsed from `[id, lon, lat]` tuples)
- `List<Edge> loadEdges()` - Returns a list of [Edge] objects (parsed from `[from, to, lengthNm]` tuples)
- `Meta loadMeta()` - Returns a [Meta] object with schema and units information
- `nodesData`, `edgesData`, `metaData` - Raw parsed JSON data for advanced use cases

## Models

```dart
class Node {
  final int id;
  final double lon;
  final double lat;
}

class Edge {
  final int from;
  final int to;
  final double lengthNm;
}

class Meta {
  final String distanceUnits;
  final List<String> nodeSchema;
  final List<String> edgeSchema;
}
```

## Data

- **Nodes**: parsed from tuples `[id, lon, lat]`
- **Edges**: parsed from tuples `[from, to, lengthNm]` (directed, length in nautical miles)
- **Meta**: schema + units

For more details and important “not for navigation” notes, see the main README:

- `https://github.com/ssroute/data-eurostat`

## License

EUPL-1.2 - See [LICENSE](LICENSE) for details.

Data derived from [Eurostat SeaRoute / MARNET](https://github.com/eurostat/searoute).
