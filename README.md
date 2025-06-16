# Create db format with puml to get table relations

## 1. create db format

```bash
./scripts/relations/generate_plantuml.sh
```

## 2. create subgraphs

```bash
./scripts/relations/extract_subgraph.sh
```
example
```bash
python scripts/relations/extract_subgraph.py --puml database_diagram_simple.puml --tables Projects Contracts
```

# SQL: Create local database & query it with SqlAlchemy

## 1. create local db on your machine

```bash
./scripts/local_db/create_local_sqldb.sh
```

## 2. build tables
```bash
./scripts/local_db/create_tables_sql.sh
```

# Postgress: Create local database & query it with SqlAlchemy

## 1. create local db on your machine

```bash
./scripts/local_db/create_local_pg.sh
```

## 2. build tables
```bash
./scripts/local_db/create_tables_pg.sh
```