Eurostat SeaRoute Maritime Graph (JSON)
=======================================

This repository publishes a language-agnostic sea-routing graph derived from Eurostat’s SeaRoute / MARNET maritime network. The data is provided in a simple JSON-based format so any routing library can consume it without depending on a specific language or framework.

What’s inside
-------------
- Nodes: unique waypoints on the sea surface, each with `id`, `lon`, and `lat`.
- Edges: directed connections between nodes, each with `from`, `to`, and `length_nm` (great-circle distance of the segment, in nautical miles).
- Meta: a small metadata file describing schema, units, and the upstream source.

Scope
-----
This is pure data. No routing algorithms are included. Client libraries can build adjacency structures and run Dijkstra, A*, or any other graph search on top of this graph to compute shortest sea routes between origins and destinations.

Provenance and license
----------------------
The dataset is a processed derivative of Eurostat’s SeaRoute / MARNET maritime network (`marnet.gpkg`). It introduces no new source data—only a change of representation (GeoPackage → JSON graph). In line with the upstream project, the data is distributed under the EUPL-1.2 license.

Credits
-------
- Upstream network and project: https://github.com/eurostat/searoute

Usage notes
-----------
- Nodes and edges are stored as JSON; see `data/` for the graph files.
- Length units: nautical miles (`length_nm`).
- Coordinate reference: longitude, latitude in decimal degrees (WGS84).

