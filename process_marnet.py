#!/usr/bin/env python3
"""
Process Eurostat Marnet GPKG file to extract network graph data.

Downloads marnet.gpkg, extracts nodes and edges from the "type" layer,
and outputs JSON files with the network graph representation.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import fiona
import geopandas as gpd
import requests
from shapely.geometry import LineString, MultiLineString

# Constants
GPKG_URL = "https://github.com/eurostat/searoute/raw/refs/heads/master/modules/marnet/src/main/resources/marnet.gpkg"
GPKG_FILENAME = "marnet.gpkg"
LAYER_NAME = "type"
COORDINATE_PRECISION = 6
MIN_COORDS_FOR_LINE = 2
EXPECTED_NODE_ELEMENTS = 3
EXPECTED_EDGE_ELEMENTS = 3
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0


def download_gpkg(url: str, output_path: str) -> None:
    """
    Download GPKG file from URL and save to output path.

    Args:
        url: URL to download from
        output_path: Path to save the downloaded file
    """
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    output_path_obj = Path(output_path)
    with output_path_obj.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end="", flush=True)

    print(f"\nDownloaded {output_path} ({downloaded / 1024 / 1024:.2f} MB)")


def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using Haversine formula.

    Args:
        lon1: Longitude of first point in degrees
        lat1: Latitude of first point in degrees
        lon2: Longitude of second point in degrees
        lat2: Latitude of second point in degrees

    Returns:
        Distance in nautical miles
    """
    # Earth radius in nautical miles
    r = 3438.9

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def calculate_polyline_length(coords: List[Tuple[float, float]]) -> float:
    """
    Calculate the total length of a polyline by summing Haversine distances
    between consecutive vertices.

    Args:
        coords: List of (lon, lat) coordinate tuples

    Returns:
        Total length in nautical miles
    """
    if len(coords) < MIN_COORDS_FOR_LINE:
        return 0.0

    total_length = 0.0
    for i in range(len(coords) - 1):
        lon1, lat1 = coords[i]
        lon2, lat2 = coords[i + 1]
        total_length += haversine_distance(lon1, lat1, lon2, lat2)

    return total_length


def round_coord(coord: float) -> float:
    """Round coordinate to specified precision."""
    return round(coord, COORDINATE_PRECISION)


def extract_nodes_and_edges(gdf: gpd.GeoDataFrame) -> Tuple[List[List], List[List]]:
    """
    Extract nodes and edges from GeoDataFrame containing LineString/MultiLineString geometries.

    Args:
        gdf: GeoDataFrame with geometry column

    Returns:
        Tuple of (nodes_list, edges_list)
    """
    # Dictionary to map (lon, lat) tuples to node IDs
    coord_to_node_id: Dict[Tuple[float, float], int] = {}
    nodes_list: List[List] = []
    edges_list: List[List] = []
    node_id_counter = 0

    def get_or_create_node(lon: float, lat: float) -> int:
        """Get existing node ID or create new node."""
        nonlocal node_id_counter
        coord_key = (round_coord(lon), round_coord(lat))

        if coord_key not in coord_to_node_id:
            coord_to_node_id[coord_key] = node_id_counter
            nodes_list.append([node_id_counter, coord_key[0], coord_key[1]])
            node_id_counter += 1

        return coord_to_node_id[coord_key]

    def process_linestring(geom: LineString) -> None:
        """Process a single LineString geometry."""
        coords = list(geom.coords)
        if len(coords) < MIN_COORDS_FOR_LINE:
            return

        # Get start and end coordinates
        start_lon, start_lat = coords[0]
        end_lon, end_lat = coords[-1]

        # Get or create nodes
        from_id = get_or_create_node(start_lon, start_lat)
        to_id = get_or_create_node(end_lon, end_lat)

        # Calculate length
        length_nm = calculate_polyline_length(coords)

        # Add edge
        edges_list.append([from_id, to_id, round(length_nm, 6)])

    # Process all geometries
    print(f"Processing {len(gdf)} features...")
    for idx, row in gdf.iterrows():
        geom = row.geometry

        if geom is None or geom.is_empty:
            continue

        if isinstance(geom, LineString):
            process_linestring(geom)
        elif isinstance(geom, MultiLineString):
            # Process each LineString part separately
            for linestring in geom.geoms:
                process_linestring(linestring)
        else:
            print(f"Warning: Unsupported geometry type {type(geom).__name__} at index {idx}")

    return nodes_list, edges_list


def validate_nodes(nodes: List[List]) -> None:
    """
    Validate nodes data structure and values.

    Args:
        nodes: List of node tuples [id, lon, lat]

    Raises:
        ValueError: If validation fails
    """
    if not nodes:
        msg = "Nodes list is empty"
        raise ValueError(msg)

    node_ids = set()
    for idx, node in enumerate(nodes):
        # Check structure
        if not isinstance(node, list):
            msg = f"Node at index {idx} is not a list: {type(node).__name__}"
            raise TypeError(msg)
        if len(node) != EXPECTED_NODE_ELEMENTS:
            msg = f"Node at index {idx} has {len(node)} elements, expected {EXPECTED_NODE_ELEMENTS}: {node}"
            raise ValueError(msg)

        # Extract and validate fields
        try:
            node_id = int(node[0])
            lon = float(node[1])
            lat = float(node[2])
        except (ValueError, TypeError, IndexError) as e:
            msg = f"Node at index {idx} has invalid types: {node}"
            raise ValueError(msg) from e

        # Validate ID
        if node_id != idx:
            msg = f"Node at index {idx} has ID {node_id}, expected {idx}"
            raise ValueError(msg)

        # Check for duplicate IDs
        if node_id in node_ids:
            msg = f"Duplicate node ID {node_id} found at index {idx}"
            raise ValueError(msg)
        node_ids.add(node_id)

        # Validate coordinates
        if not (MIN_LONGITUDE <= lon <= MAX_LONGITUDE):
            msg = f"Node {node_id} has invalid longitude {lon}, must be between {MIN_LONGITUDE} and {MAX_LONGITUDE}"
            raise ValueError(msg)
        if not (MIN_LATITUDE <= lat <= MAX_LATITUDE):
            msg = f"Node {node_id} has invalid latitude {lat}, must be between {MIN_LATITUDE} and {MAX_LATITUDE}"
            raise ValueError(msg)

    print(f"✓ Validated {len(nodes)} nodes: all IDs unique, coordinates in valid ranges")


def validate_edges(edges: List[List], node_ids: set) -> None:
    """
    Validate edges data structure and values.

    Args:
        edges: List of edge tuples [fromId, toId, lengthNm]
        node_ids: Set of valid node IDs from nodes list

    Raises:
        ValueError: If validation fails
    """
    if not edges:
        msg = "Edges list is empty"
        raise ValueError(msg)

    max_node_id = max(node_ids) if node_ids else -1

    for idx, edge in enumerate(edges):
        # Check structure
        if not isinstance(edge, list):
            msg = f"Edge at index {idx} is not a list: {type(edge).__name__}"
            raise TypeError(msg)
        if len(edge) != EXPECTED_EDGE_ELEMENTS:
            msg = f"Edge at index {idx} has {len(edge)} elements, expected {EXPECTED_EDGE_ELEMENTS}: {edge}"
            raise ValueError(msg)

        # Extract and validate fields
        try:
            from_id = int(edge[0])
            to_id = int(edge[1])
            length_nm = float(edge[2])
        except (ValueError, TypeError, IndexError) as e:
            msg = f"Edge at index {idx} has invalid types: {edge}"
            raise ValueError(msg) from e

        # Validate node references
        if from_id not in node_ids:
            msg = f"Edge at index {idx} references invalid 'from' node ID {from_id} (max valid ID: {max_node_id})"
            raise ValueError(msg)
        if to_id not in node_ids:
            msg = f"Edge at index {idx} references invalid 'to' node ID {to_id} (max valid ID: {max_node_id})"
            raise ValueError(msg)

        # Validate length
        if length_nm < 0:
            msg = f"Edge at index {idx} has negative length {length_nm}, must be >= 0"
            raise ValueError(msg)
        if not math.isfinite(length_nm):
            msg = f"Edge at index {idx} has non-finite length {length_nm}"
            raise ValueError(msg)

    print(f"✓ Validated {len(edges)} edges: all node references valid, lengths non-negative")


def write_output_files(nodes: List[List], edges: List[List], project_root: Path) -> None:
    """
    Write nodes.json, edges.json, and meta.json to data folder.

    Args:
        nodes: List of node tuples [id, lon, lat]
        edges: List of edge tuples [fromId, toId, lengthNm]
        project_root: Project root directory
    """
    # Validate data before writing
    print("\nValidating data...")
    validate_nodes(nodes)
    node_ids = {node[0] for node in nodes}
    validate_edges(edges, node_ids)

    # Create data directory
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Write nodes.json to data folder
    nodes_path = data_dir / "nodes.json"
    with nodes_path.open("w") as f:
        json.dump(nodes, f, separators=(",", ":"))
    print(f"Written {len(nodes)} nodes to {nodes_path}")

    # Write edges.json to data folder
    edges_path = data_dir / "edges.json"
    with edges_path.open("w") as f:
        json.dump(edges, f, separators=(",", ":"))
    print(f"Written {len(edges)} edges to {edges_path}")

    # Write meta.json to data folder
    meta = {
        "distance_units": "nm",
        "node_schema": ["id", "lon", "lat"],
        "edge_schema": ["from", "to", "length_nm"]
    }
    meta_path = data_dir / "meta.json"
    with meta_path.open("w") as f:
        json.dump(meta, f, indent=2)
    print(f"Written metadata to {meta_path}")


def main():
    """Main processing function."""
    # Get project root directory
    project_root = Path(__file__).parent

    # Download GPKG file
    gpkg_path = project_root / GPKG_FILENAME
    if not gpkg_path.exists():
        download_gpkg(GPKG_URL, str(gpkg_path))
    else:
        print(f"Using existing {gpkg_path}")

    # Read the "type" layer
    print(f"Reading layer '{LAYER_NAME}' from {gpkg_path}...")
    try:
        gdf = gpd.read_file(str(gpkg_path), layer=LAYER_NAME)
    except ValueError as e:
        print(f"Error reading layer '{LAYER_NAME}': {e}")
        print("Available layers:")
        layers = fiona.listlayers(str(gpkg_path))
        for layer in layers:
            print(f"  - {layer}")
        raise

    print(f"Loaded {len(gdf)} features from layer '{LAYER_NAME}'")

    # Extract nodes and edges
    nodes, edges = extract_nodes_and_edges(gdf)

    print(f"\nExtracted {len(nodes)} unique nodes and {len(edges)} edges")

    # Write output files (nodes and edges to data folder, meta to root)
    write_output_files(nodes, edges, project_root)

    print("\nProcessing complete!")


if __name__ == "__main__":
    main()

