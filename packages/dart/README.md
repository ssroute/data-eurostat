# ssroute_data_eurostat

Eurostat SeaRoute / MARNET maritime routing graph data (GeoJSON) for Dart (VM/CLI/server).

## Usage

```dart
import 'package:ssroute_data_eurostat/ssroute_data_eurostat.dart';

void main() async {
  final nodes = await loadNodes();
  final edges = await loadEdges();
  final meta = await loadMeta();

  print('Loaded ${nodes['features'].length} nodes');
  print('Loaded ${edges['features'].length} edges');
}
```

## API

- `Future<Map<String, dynamic>> loadNodes()` - Returns the nodes GeoJSON FeatureCollection
- `Future<Map<String, dynamic>> loadEdges()` - Returns the edges GeoJSON FeatureCollection
- `Future<Map<String, dynamic>> loadMeta()` - Returns the metadata JSON (schema, units, etc.)

## Data

- **Nodes**: Unique waypoints on the sea surface, each with `id`, `lon`, and `lat`.
- **Edges**: Directed connections between nodes, each with `from`, `to`, and `length_nm` (nautical miles).
- **Meta**: Metadata describing schema, units, and the upstream source.

## License

EUPL-1.2 - See [LICENSE](LICENSE) for details.

Data derived from [Eurostat SeaRoute / MARNET](https://github.com/eurostat/searoute).
