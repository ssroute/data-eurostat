// Simple accessors for the embedded graph data.
// Assumes ../data/*.geojson + meta.json are copied into ./data by scripts/release.py.

const fs = require("node:fs");
const path = require("node:path");

function readJson(file) {
  const p = path.join(__dirname, "data", file);
  const raw = fs.readFileSync(p, "utf8");
  return JSON.parse(raw);
}

/**
 * Returns the nodes GeoJSON FeatureCollection.
 */
function getNodes() {
  return readJson("nodes.geojson");
}

/**
 * Returns the edges GeoJSON FeatureCollection.
 */
function getEdges() {
  return readJson("edges.geojson");
}

/**
 * Returns the metadata JSON (schema, units, etc.).
 */
function getMeta() {
  return readJson("meta.json");
}

module.exports = {
  getNodes,
  getEdges,
  getMeta
};

