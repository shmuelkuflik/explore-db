set -e
set -x

echo "START create_tables.sh [$(date)]"

for file_name in ITST_Test_1_dbo_PrototypeVersionsRegions ITST_Test_1_dbo_Regions; do
  sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -d master -i ./scripts/local_db/sql/create_${file_name}.sql
  sed -i '' 's/,true/,1/g; s/,false/,0/g' tmp/tables/${file_name}.csv
  docker cp tmp/tables/${file_name}.csv sqlserver:/tmp/${file_name}.csv
  sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' \
    -d master -v FILE_NAME="${file_name}" \
    -i scripts/local_db/sql/import_csv.sql
  exit
done

echo "END create_tables.sh [$(date)]"
