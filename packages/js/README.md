# @ssroute/data-eurostat

Eurostat SeaRoute / MARNET maritime routing graph data (GeoJSON) for JavaScript/TypeScript.

## Installation

```bash
npm install @ssroute/data-eurostat
```

## Usage

```javascript
const { getNodes, getEdges, getMeta } = require('@ssroute/data-eurostat');

const nodes = getNodes();
const edges = getEdges();
const meta = getMeta();

console.log(`Loaded ${nodes.features.length} nodes`);
console.log(`Loaded ${edges.features.length} edges`);
```

## API

- `getNodes()` - Returns the nodes GeoJSON FeatureCollection
- `getEdges()` - Returns the edges GeoJSON FeatureCollection
- `getMeta()` - Returns the metadata JSON (schema, units, etc.)

## Data

- **Nodes**: Unique waypoints on the sea surface, each with `id`, `lon`, and `lat`.
- **Edges**: Directed connections between nodes, each with `from`, `to`, and `length_nm` (nautical miles).
- **Meta**: Metadata describing schema, units, and the upstream source.

## License

EUPL-1.2 - See [LICENSE](LICENSE) for details.

Data derived from [Eurostat SeaRoute / MARNET](https://github.com/eurostat/searoute).
