// Simple accessors for the embedded graph data.
// Data is embedded at build time - works in both browser and Node.js.
// Assumes ../data/*.json + meta.json are copied into ./data by scripts/release.py.

import nodesData from "./data/nodes.json";
import edgesData from "./data/edges.json";
import metaData from "./data/meta.json";

export type Node = [id: number, lon: number, lat: number];
export type Edge = [from: number, to: number, lengthNm: number];
export type Meta = {
  distance_units: "nm";
  node_schema: ["id", "lon", "lat"];
  edge_schema: ["from", "to", "length_nm"];
};

/**
 * Returns the nodes as an array of tuples [id, lon, lat].
 * Works in both browser and Node.js environments.
 */
export function getNodes(): Node[] {
  return nodesData as Node[];
}

/**
 * Returns the edges as an array of tuples [from, to, lengthNm].
 * Works in both browser and Node.js environments.
 */
export function getEdges(): Edge[] {
  return edgesData as Edge[];
}

/**
 * Returns the metadata JSON (schema, units, etc.).
 * Works in both browser and Node.js environments.
 */
export function getMeta(): Meta {
  return metaData as Meta;
}

// Export raw data for advanced use cases (e.g., custom bundling, tree-shaking)
export { nodesData, edgesData, metaData };

