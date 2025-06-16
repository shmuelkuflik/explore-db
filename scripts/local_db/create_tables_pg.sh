#!/bin/bash
set -e
#set -x

echo "START create_tables.sh [$(date)]"

# Connection variables
PGHOST=127.0.0.1
PGUSER=postgres
PGPASSWORD=yourStrongPassword
PGDATABASE=localdb

export PGPASSWORD  # ensures psql uses the password non-interactively

for file_name in PrototypeVersionsRegions PrototypeVersions BackendPrototypeEnvs Regions; do
  psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -c "DROP TABLE IF EXISTS \"${file_name}\";"
done

for file_name in Regions BackendPrototypeEnvs PrototypeVersions PrototypeVersionsRegions; do
  # Create tables
  psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -f "./scripts/local_db/pg/${file_name}.sql"
done

echo "+++++ Start fill tables with data +++++"
for file_name in Regions BackendPrototypeEnvs PrototypeVersions PrototypeVersionsRegions; do
  csv_file="tmp/tables/${file_name}.csv"
  # Copy the CSV into the container
  if [ -f "${csv_file}" ]; then
    # Replace 'true'/'false' with 1/0 in CSV (for PostgreSQL boolean compatibility if needed)
    sed -i '' 's/,true/,1/g; s/,false/,0/g' "${csv_file}"
    echo "Copying ${file_name}.csv to PostgreSQL container"
    docker cp "${csv_file}" postgres:/tmp/${file_name}.csv
    # Import CSV using psql inside the container
    docker exec -u postgres postgres \
      psql -d localdb \
      -c "\copy \"${file_name}\" FROM '/tmp/${file_name}.csv' WITH (FORMAT csv, HEADER, DELIMITER ',')"

  else
    echo "File ${csv_file} does not exist. Skipping copy."
    continue
  fi
done

echo "END create_tables.sh [$(date)]"
