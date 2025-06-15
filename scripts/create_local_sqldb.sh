set -e
set -x

echo "START create_local_sqlbb.sh [$(date)]"

# shellcheck disable=SC2157
if [ -n "${1}" ]; then
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  if [[ "$(uname)" == "Darwin" ]]; then
    brew install unixodbc
    brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
    brew update
    HOMEBREW_NO_AUTO_UPDATE=1 brew install msodbcsql17
    odbcinst -q -d
  fi
fi

if lsof -i :1433 >/dev/null 2>&1; then
  echo "Port 1433 is already in use. Stopping and removing existing SQL Server container..."
  docker stop sqlserver || true
  docker rm sqlserver || true
else
  echo "Port 1433 is free. Proceeding to create SQL Server container..."
fi

odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

# Start SQL Server container if it's not already running
docker run --platform linux/amd64 \
  -e ACCEPT_EULA=Y \
  -e 'SA_PASSWORD=YourStrong!Passw0rd' \
  -e MSSQL_PID=Developer \
  -p 1433:1433 \
  --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest

# Wait a few seconds for SQL Server to start up
echo "Waiting for SQL Server to start..."
sleep 10

# Test with sqlcmd (optional, can skip in CI)
#docker run -it --rm \
#  --add-host=host.docker.internal:host-gateway \
#  ghcr.io/marcopas/docker-mssql-tools \
#  sqlcmd -S host.docker.internal -U sa -P 'YourStrong!Passw0rd' -Q "SELECT @@VERSION"
sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -Q "SELECT @@VERSION"

docker ps
lsof -iTCP:1433

echo "END create_local_sqlbb.sh [$(date)]"