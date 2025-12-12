Eurostat SeaRoute Maritime Graph (JSON)
=======================================

This repository publishes a language-agnostic sea-routing graph derived from Eurostat’s SeaRoute / MARNET maritime network. The data is provided in a simple JSON-based format so any routing library can consume it without depending on a specific language or framework.

Explain it like I’m 5
---------------------
Imagine the sea has a bunch of **invisible stepping stones** you’re allowed to “hop” between.
Those stepping stones are **nodes**.
And the hops between them are **edges**.

- **Nodes are dots on the map**: each node has an `id` and a location (`lon`, `lat`).
- **Edges are allowed hops**: each edge says “you can go from node A to node B” and how long that hop is (`length_nm`).

If you want to draw a path from one place to another, you don’t draw any random line across the ocean.
Instead you:

1. **Pick a start node** near your starting point.
2. **Pick an end node** near your destination.
3. Let a path-finding algorithm choose which hops to take.
4. **Draw the result** by connecting the visited nodes into a polyline.

The important bit: this produces **realistic-looking sea routes for visualization**, because the hops follow the same network structure used by the upstream maritime graph.

What this is (and is not)
-------------------------
- **This IS** a graph dataset meant for **maps, demos, analytics, and route visualizations** (e.g. “draw plausible shipping lanes between ports”).
- **This is NOT** a marine navigation product. Do **not** use it for real-world routing, voyage planning, safety, or decision-making.

What’s inside
-------------
- Nodes: unique waypoints on the sea surface, each with `id`, `lon`, and `lat`.
- Edges: directed connections between nodes, each with `from`, `to`, and `length_nm` (great-circle distance of the segment, in nautical miles).
- Meta: a small metadata file describing schema, units, and the upstream source.

How Dijkstra / A* can use this data
-----------------------------------
This dataset is a **weighted directed graph**:

- **Vertices (nodes)**: the waypoint points.
- **Directed edges**: allowed transitions from `from` → `to`.
- **Weights**: `length_nm` is the cost of traversing that edge.

Routing algorithms like **Dijkstra** and **A\*** don’t need “sea knowledge” — they just need a graph.
They repeatedly expand the cheapest next hop until they reach the destination:

- **Dijkstra**: uses edge weights only (finds the globally shortest path by total `length_nm`).
- **A\***: uses edge weights **plus a heuristic** (usually straight-line distance from the current node to the goal) to speed things up.

Typical visualization workflow:

1. **Snap endpoints**: map your origin/destination coordinates (ports, cities, clicks on a map) to the nearest graph nodes.
2. **Build adjacency**: from the edge list, build a `from -> [(to, length_nm), ...]` neighbor list.
3. **Run a shortest-path search**: Dijkstra or A\* to get the sequence of node ids.
4. **Render the route**: replace node ids with `(lon, lat)` coordinates and draw a line on your map.

Note: “realistic-looking” here means **consistent with the network geometry** — it does not mean “safe” or “operationally correct”.

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
- Edges are **directed**: treat them as one-way links unless the reverse edge also exists.

Packages
--------
This repository is the canonical source for the graph data, with two thin packages that embed and expose the data:

- **NPM**: `@ssroute/data-eurostat` (in `packages/js/`)
- **Dart**: `ssroute_data_eurostat` (in `packages/dart/`)

Release workflow
----------------
To cut a new data release:

1. Update files under `data/` as needed.
2. Bump the version in the root `VERSION` file (e.g. `0.2.0`).
3. Run: `python scripts/release.py`
4. Commit and tag:
   ```
   git commit -am "Release v0.2.0"
   git tag v0.2.0 && git push && git push --tags
   ```
5. Publish:
   - `cd packages/js && npm publish --access public`
   - `cd packages/dart && dart pub publish`

