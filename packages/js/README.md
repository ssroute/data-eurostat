# @ssroute/data-eurostat

Eurostat SeaRoute / MARNET maritime routing graph data (JSON tuples) for JavaScript/TypeScript.

**Works in both browser and Node.js** - data is embedded at build time, no file I/O required.

For a plain-language explanation of the dataset (ELI5), data structure, and how it can be used with Dijkstra/A* for *visualizations* (not navigation), see the main repository README:

- `https://github.com/ssroute/data-eurostat#explain-it-like-im-5`

## Installation

```bash
npm install @ssroute/data-eurostat
```

## Usage

### TypeScript / ES Modules

```typescript
import { getNodes, getEdges, getMeta, type Node, type Edge, type Meta } from '@ssroute/data-eurostat';

const nodes: Node[] = getNodes();
const edges: Edge[] = getEdges();
const meta: Meta = getMeta();

console.log(`Loaded ${nodes.length} nodes`);
console.log(`Loaded ${edges.length} edges`);
console.log(`Distance units: ${meta.distance_units}`);
```

### JavaScript / CommonJS

```javascript
const { getNodes, getEdges, getMeta } = require('@ssroute/data-eurostat');

const nodes = getNodes();
const edges = getEdges();
const meta = getMeta();
```

### Advanced: Direct Data Access

For custom bundling or tree-shaking:

```typescript
import { nodesData, edgesData, metaData } from '@ssroute/data-eurostat';

// Access raw data arrays directly
const firstNode = nodesData[0];
```

## API

- `getNodes(): Node[]` - Returns an array of node tuples `[id, lon, lat]`
- `getEdges(): Edge[]` - Returns an array of edge tuples `[from, to, lengthNm]`
- `getMeta(): Meta` - Returns the metadata object (schema, units, etc.)
- `nodesData`, `edgesData`, `metaData` - Raw data exports for advanced use cases

## Types

```typescript
type Node = [id: number, lon: number, lat: number];
type Edge = [from: number, to: number, lengthNm: number];
type Meta = {
  distance_units: "nm";
  node_schema: ["id", "lon", "lat"];
  edge_schema: ["from", "to", "length_nm"];
};
```

## Data

- **Nodes**: tuples `[id, lon, lat]`
- **Edges**: tuples `[from, to, lengthNm]` (directed, length in nautical miles)
- **Meta**: schema + units

For more details and important “not for navigation” notes, see the main README:

- `https://github.com/ssroute/data-eurostat`

## License

EUPL-1.2 - See [LICENSE](LICENSE) for details.

Data derived from [Eurostat SeaRoute / MARNET](https://github.com/eurostat/searoute).
