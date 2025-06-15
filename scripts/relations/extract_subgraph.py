import networkx as nx


def parse_puml_file(file_path):
    """
    Parse the .puml file to extract tables, columns, and relationships.
    """
    graph = nx.DiGraph()
    table_columns = {}
    current_table = None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Detect start of a class/table
            if line.startswith("class "):
                current_table = line.split()[1]
                table_columns[current_table] = []
                graph.add_node(current_table)

            # Detect end of class
            elif line == "}":
                current_table = None

            # Collect column definitions
            elif current_table and ":" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    column_name = parts[0].strip()
                    column_type = parts[1].strip()
                    table_columns[current_table].append((column_name, column_type))

            # Parse relationships
            elif "-->" in line:
                parts = line.split("-->")
                src = parts[0].strip()
                dst = parts[1].strip()
                graph.add_edge(src, dst)

    return graph, table_columns


def extract_subgraph(graph, tables):
    """
    Return a subgraph including the paths between all given tables,
    or just the neighborhood if only one table is provided.
    """
    if not tables:
        return None

    if len(tables) == 1:
        t = tables[0]
        if t in graph:
            neighbors = list(graph.successors(t)) + list(graph.predecessors(t))
            return graph.subgraph([t] + neighbors).copy()
        else:
            print(f"Table {t} not found in graph")
            return None

    # Multiple tables: find all shortest paths between pairs
    nodes = set()
    try:
        for i in range(len(tables)):
            for j in range(i + 1, len(tables)):
                t1, t2 = tables[i], tables[j]
                if t1 in graph and t2 in graph:
                    paths = nx.all_shortest_paths(graph.to_undirected(), t1, t2)
                    for path in paths:
                        nodes.update(path)
                else:
                    print(f"Skipping path between {t1} and {t2} (one or both tables not found)")
        return graph.subgraph(nodes).copy() if nodes else None
    except nx.NetworkXNoPath:
        print(f"No path between some of the specified tables")
        return None


def export_subgraph_to_puml(subgraph, table_columns, output_file, include_columns=True, highlight_tables=None):
    """
    Export the subgraph to a .puml format with optional column display and highlighted tables.
    """
    highlight_tables = set(highlight_tables or [])

    with open(output_file, 'w') as f:
        f.write("@startuml\n\n")
        f.write("skinparam class {\n")
        f.write("  BackgroundColor White\n")
        f.write("  BorderColor Black\n")
        f.write("}\n\n")

        # Highlight style for main tables
        f.write("hide empty members\n\n")  # optional: hides empty member boxes

        for node in subgraph.nodes:
            style = ""
            if node in highlight_tables:
                style = " #LightBlue"  # Or use <<highlight>> stereotype and define styles

            if include_columns:
                f.write(f"class {node}{style} {{\n")
                for col in table_columns.get(node, []):
                    if isinstance(col, tuple) and len(col) == 2:
                        f.write(f"  {col[0]} : {col[1]}\n")
                    else:
                        f.write(f"  {col} : unknown\n")  # fallback if data is malformed
                f.write("}\n\n")
            else:
                f.write(f"class {node}{style}\n")

        for src, dst in subgraph.edges:
            f.write(f"{src} --> {dst}\n")

        f.write("\n@enduml\n")
    print(f"Subgraph written to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract subgraph from PlantUML file")
    parser.add_argument("--puml", required=True, help="Path to database_diagram_simple.puml")
    parser.add_argument("--tables", nargs="+", required=True, help="List of table names to extract relationships between")
    parser.add_argument("--no-columns", action="store_true", help="Exclude columns in output")

    args = parser.parse_args()

    base_path = "tmp"
    graph, table_columns = parse_puml_file(f"{base_path}/{args.puml}")
    subgraph = extract_subgraph(graph, args.tables)

    if subgraph:
        export_subgraph_to_puml(
            subgraph,
            table_columns,
            output_file=f"{base_path}/subgraph.puml",
            include_columns=not args.no_columns,
            highlight_tables=args.tables
        )
