set -e
#set -x

echo "START create_tables.sh [$(date)]"

for file_name in PrototypeVersionsRegions Regions; do
  echo "Dropping table ${file_name} if it exists..."
  sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -d master -Q "IF OBJECT_ID('dbo.${file_name}', 'U') IS NOT NULL DROP TABLE dbo.${file_name};"
done

for file_name in Regions PrototypeVersionsRegions; do
  if [ -f "./scripts/local_db/sql/create_${file_name}.sql" ];then
    echo "Creating table ${file_name}..."
    sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -d master -i ./scripts/local_db/sql/create_${file_name}.sql
  fi
done

echo "+++++ Start fill tables with data +++++"
for file_name in Regions PrototypeVersionsRegions; do
  csv_file="tmp/tables/${file_name}.csv"
  if [ -f "${csv_file}" ];then
    echo "fill ${file_name} table with data from ${csv_file}"
#    sed -i '' 's/,true/,1/g; s/,false/,0/g' ${csv_file}
    docker cp ${csv_file} sqlserver:/tmp/${file_name}.csv
    sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' \
      -d master -v FILE_NAME="${file_name}" \
      -i scripts/local_db/sql/import_csv.sql
  fi
done

echo "END create_tables.sh [$(date)]"
