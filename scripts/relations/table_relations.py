import csv
from collections import defaultdict, deque

# Load foreign key relations from CSV
foreign_keys = []
with open('scripts/relations/sql/table_relations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        parent = row['PARENT_TABLE'].strip()
        referenced = row['REFERENCED_TABLE'].strip()
        foreign_keys.append( (parent, referenced) )

# Step 1: Build graph
graph = defaultdict(list)
in_degree = defaultdict(int)
tables = set()

for parent, referenced in foreign_keys:
    graph[referenced].append(parent)
    in_degree[parent] += 1
    tables.add(parent)
    tables.add(referenced)

# Ensure all tables are present in in_degree
for t in tables:
    in_degree.setdefault(t, 0)

# Step 2: Topological sort
queue = deque([t for t in tables if in_degree[t] == 0])
layers = []
visited = set()

while queue:
    current_layer = list(queue)
    layers.append(current_layer)
    next_queue = deque()

    while queue:
        table = queue.popleft()
        visited.add(table)
        for dependent in graph[table]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                next_queue.append(dependent)

    queue = next_queue

# Check for cycles
if len(visited) != len(tables):
    raise Exception("Cycle detected in foreign key relationships!")

# Output
for i, layer in enumerate(layers, 1):
    print(f"{i}. {', '.join(sorted(layer))}")
