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
                column = line.split(":")[0].strip()
                table_columns[current_table].append(column)

            # Parse relationships
            elif "-->" in line:
                parts = line.split("-->")
                src = parts[0].strip()
                dst = parts[1].strip()
                graph.add_edge(src, dst)

    return graph, table_columns


def extract_subgraph(graph, table1, table2=None):
    """
    Return a subgraph including the path(s) between table1 and table2,
    or just neighbors of table1 if table2 is None.
    """
    if table2 and table1 in graph and table2 in graph:
        try:
            paths = nx.all_shortest_paths(graph.to_undirected(), table1, table2)
            nodes = set()
            edges = set()
            for path in paths:
                for i in range(len(path) - 1):
                    nodes.update([path[i], path[i + 1]])
                    edges.add((path[i], path[i + 1]))
            return graph.subgraph(nodes).copy()
        except nx.NetworkXNoPath:
            print(f"No path between {table1} and {table2}")
            return None
    elif table1 in graph:
        neighbors = list(graph.successors(table1)) + list(graph.predecessors(table1))
        return graph.subgraph([table1] + neighbors).copy()
    else:
        print(f"Table {table1} not found in graph")
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
                    f.write(f"  {col} : unknown\n")
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
    parser.add_argument("--table1", required=True, help="First table name")
    parser.add_argument("--table2", help="Second table name (optional)")
    parser.add_argument("--no-columns", action="store_true", help="Exclude columns in output")

    args = parser.parse_args()

    base_path = "tmp"
    graph, table_columns = parse_puml_file(f"{base_path}/{args.puml}")
    subgraph = extract_subgraph(graph, args.table1, args.table2)

    if subgraph:
        export_subgraph_to_puml(
            subgraph,
            table_columns,
            output_file=f"{base_path}/subgraph.puml",
            include_columns=not args.no_columns,
            highlight_tables=[args.table1] + ([args.table2] if args.table2 else [])
        )

