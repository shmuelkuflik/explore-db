#!/bin/bash
set -e
set -x

echo "START create_local_postgres.sh [$(date)]"

# shellcheck disable=SC2157
if [ -n "${1}" ]; then
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  if [[ "$(uname)" == "Darwin" ]]; then
    brew install unixodbc
    brew install psqlodbc  # PostgreSQL ODBC driver
    odbcinst -q -d
  fi
fi

if lsof -i :5432 >/dev/null 2>&1; then
  echo "Port 5432 is already in use. Stopping and removing existing PostgreSQL container..."
  docker stop postgres || true
  docker rm postgres || true
else
  echo "Port 5432 is free. Proceeding to create PostgreSQL container..."
fi

cp scripts/local_db/odbcinst.ini /opt/homebrew/etc/
# brew install psqlodbc
odbcinst -q -d -n "PostgreSQL"

# Start PostgreSQL container
docker run --platform linux/amd64 \
  -e POSTGRES_PASSWORD=yourStrongPassword \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=localdb \
  -p 5432:5432 \
  --name postgres \
  -d postgres:16

echo "Waiting for PostgreSQL to start..."
sleep 10

# Test the connection using psql (needs to be installed via brew: brew install postgresql)
PGPASSWORD=yourStrongPassword psql -h 127.0.0.1 -U postgres -d localdb -c "SELECT version();"

docker ps
lsof -iTCP:5432

echo "END create_local_postgres.sh [$(date)]"
