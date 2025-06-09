import pandas as pd
from collections import defaultdict
import os


def generate_complete_plantuml_diagram(base_input_path):
    """
    Generate complete PlantUML class diagram from all CSV files
    """

    # File paths
    files = {
        'columns': f"{base_input_path}/1__Get_all_tables_anlumns_with_basic_info.csv",
        'primary_keys': f"{base_input_path}/2__Get_Primary_Keys.csv",
        'foreign_keys': f"{base_input_path}/3__Get_Foreign_Keys_with_relationships.csv",
        'unique_constraints': f"{base_input_path}/4__Get_Unique_Constraints.csv",
        'check_constraints': f"{base_input_path}/5__Get_Check_Constraints.csv",
        'indexes': f"{base_input_path}/6__Get_Indexes__for_ing_of_relationships.csv"
    }

    # Check if files exist
    for name, path in files.items():
        if not os.path.exists(path):
            print(f"Warning: {name} file not found at {path}")

    try:
        # Read all CSV files
        print("Loading CSV files...")
        df_columns = pd.read_csv(files['columns'])
        df_pk = pd.read_csv(files['primary_keys']) if os.path.exists(files['primary_keys']) else pd.DataFrame()
        df_fk = pd.read_csv(files['foreign_keys']) if os.path.exists(files['foreign_keys']) else pd.DataFrame()
        df_uk = pd.read_csv(files['unique_constraints']) if os.path.exists(
            files['unique_constraints']) else pd.DataFrame()

        print(f"Loaded {len(df_columns)} columns, {len(df_pk)} primary keys, {len(df_fk)} foreign keys")

        # Process the data
        tables_info = process_table_data(df_columns, df_pk, df_fk, df_uk)

        # Generate PlantUML
        plantuml_content = generate_complete_plantuml(tables_info, df_fk)

        # Save to file
        output_file = f"{base_output_path}/database_diagram.puml"
        with open(output_file, 'w') as f:
            f.write(plantuml_content)

        print(f"PlantUML diagram saved to {output_file}")
        print(f"Generated diagram for {len(tables_info)} tables")

        return plantuml_content

    except Exception as e:
        print(f"Error: {e}")
        return None


def process_table_data(df_columns, df_pk, df_fk, df_uk):
    """Process all the CSV data into a structured format"""

    # Get primary keys by table and column
    primary_keys = set()
    if not df_pk.empty:
        for _, row in df_pk.iterrows():
            primary_keys.add((row['TABLE_NAME'], row['COLUMN_NAME']))

    # Get foreign keys by table and column
    foreign_keys = set()
    if not df_fk.empty:
        for _, row in df_fk.iterrows():
            foreign_keys.add((row['PARENT_TABLE'], row['PARENT_COLUMN']))

    # Get unique constraints
    unique_keys = set()
    if not df_uk.empty:
        for _, row in df_uk.iterrows():
            unique_keys.add((row['TABLE_NAME'], row['COLUMN_NAME']))

    # Group columns by table
    tables = defaultdict(list)
    for _, row in df_columns.iterrows():
        table_name = row['TABLE_NAME']
        column_name = row['COLUMN_NAME']

        # Determine column markers
        markers = []
        if (table_name, column_name) in primary_keys:
            markers.append('PK')
        if (table_name, column_name) in foreign_keys:
            markers.append('FK')
        if (table_name, column_name) in unique_keys:
            markers.append('UK')

        column_info = {
            'name': column_name,
            'type': row['DATA_TYPE'],
            'position': row['ORDINAL_POSITION'],
            'nullable': row.get('IS_NULLABLE', 'YES'),
            'markers': markers
        }
        tables[table_name].append(column_info)

    # Sort columns by ordinal position within each table
    for table_name in tables:
        tables[table_name].sort(key=lambda x: x['position'])

    return tables


def generate_complete_plantuml(tables_info, df_fk):
    """Generate the complete PlantUML content with relationships"""

    lines = [
        "@startuml",
        "!theme plain",
        "skinparam linetype ortho",
        "skinparam class {",
        "  BackgroundColor White",
        "  BorderColor Black",
        "  ArrowColor Black",
        "}",
        ""
    ]

    # Add each table as a class
    for table_name, columns in sorted(tables_info.items()):
        lines.append(f"class {table_name} {{")

        for column in columns:
            # Build column line with markers
            column_line = f"  "

            # Add prefix symbols for key types
            if 'PK' in column['markers']:
                column_line += "+ "  # Plus for primary key
            elif 'FK' in column['markers']:
                column_line += "# "  # Hash for foreign key
            else:
                column_line += "  "  # Regular column

            # Add column name and type
            column_line += f"{column['name']} : {column['type']}"

            # Add markers as suffixes
            if column['markers']:
                marker_str = ', '.join([f"<<{marker}>>" for marker in column['markers']])
                column_line += f" {marker_str}"

            # Add nullable indicator
            if column['nullable'] == 'NO':
                column_line += " NOT NULL"

            lines.append(column_line)

        lines.append("}")
        lines.append("")  # Empty line between classes

    # Add relationships from foreign keys
    if not df_fk.empty:
        lines.append("' Foreign Key Relationships")
        relationships_added = set()  # Avoid duplicates

        for _, fk_row in df_fk.iterrows():
            parent_table = fk_row['PARENT_TABLE']
            referenced_table = fk_row['REFERENCED_TABLE']
            parent_column = fk_row['PARENT_COLUMN']
            referenced_column = fk_row['REFERENCED_COLUMN']

            # Create unique relationship identifier
            rel_id = (parent_table, referenced_table, parent_column)
            if rel_id not in relationships_added:
                # Use many-to-one relationship notation
                relationship = f"{referenced_table} ||--o{{ {parent_table} : {parent_column} -> {referenced_column}"
                lines.append(relationship)
                relationships_added.add(rel_id)

        lines.append("")

    # Add legend
    lines.extend([
        "legend top left",
        "  |= Symbol |= Meaning |",
        "  | + | Primary Key |",
        "  | # | Foreign Key |",
        "  | <<PK>> | Primary Key Marker |",
        "  | <<FK>> | Foreign Key Marker |",
        "  | <<UK>> | Unique Key Marker |",
        "endlegend",
        ""
    ])

    lines.append("@enduml")

    return "\n".join(lines)


def generate_simple_version(base_input_path, base_output_path):
    """Generate a simpler version with just tables and basic relationships"""

    try:
        # Read main files
        df_columns = pd.read_csv(f"{base_input_path}/1__Get_all_tables_anlumns_with_basic_info.csv")
        df_fk = pd.read_csv(f"{base_input_path}/3__Get_Foreign_Keys_with_relationships.csv")

        # Simple table structure
        tables = defaultdict(list)
        for _, row in df_columns.iterrows():
            tables[row['TABLE_NAME']].append({
                'name': row['COLUMN_NAME'],
                'type': row['DATA_TYPE']
            })

        lines = ["@startuml", ""]

        # Add tables
        for table_name, columns in sorted(tables.items()):
            lines.append(f"class {table_name} {{")
            for col in columns:
                lines.append(f"  {col['name']} : {col['type']}")
            lines.append("}")
            lines.append("")

        # Add relationships
        for _, fk_row in df_fk.iterrows():
            lines.append(f"{fk_row['REFERENCED_TABLE']} --> {fk_row['PARENT_TABLE']}")

        lines.append("@enduml")

        # Save simple version
        simple_output = f"{base_output_path}/database_diagram_simple.puml"
        with open(simple_output, 'w') as f:
            f.write("\n".join(lines))

        print(f"Simple diagram saved to {simple_output}")

    except Exception as e:
        print(f"Error creating simple version: {e}")


# Main execution
if __name__ == "__main__":
    print("Generating complete PlantUML database diagram...")
    base_input_path = "scripts/sql"
    base_output_path = "tmp"
    if not os.path.exists(base_output_path):
        os.makedirs(base_output_path)
    if os.path.exists(f"{base_output_path}/database_diagram.puml"):
        os.remove(f"{base_output_path}/database_diagram.puml")
    if os.path.exists(f"{base_output_path}/database_diagram_simple.puml"):
        os.remove(f"{base_output_path}/database_diagram_simple.puml")

    # Generate complete version
    result = generate_complete_plantuml_diagram(base_input_path)

    # Also generate a simple version
    print("\nGenerating simple version...")

    generate_simple_version(base_input_path, base_output_path)

    if result:
        print("\n✅ Success! Check the generated .puml files:")
        print(f"- {base_output_path}/database_diagram.puml (complete with all details)")
        print(f"- {base_output_path}/database_diagram_simple.puml (simplified version)")
        print("\nYou can open these files in:")
        print("- PlantUML online editor: http://www.plantuml.com/plantuml/uml/")
        print("- VS Code with PlantUML extension")
        print("- Any PlantUML compatible viewer")
    else:
        print("❌ Failed to generate diagram. Check the error messages above.")

