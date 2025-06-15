set -e
set -x

echo "START create_tables.sh [$(date)]"

sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -d master -i ./scripts/local_db/sql/create_regions.sql

sed -i '' 's/,true/,1/g; s/,false/,0/g' tmp/tables/ITST_Test_1_dbo_Regions.csv
docker cp tmp/tables/ITST_Test_1_dbo_Regions.csv sqlserver:/tmp/ITST_Test_1_dbo_Regions.csv
sqlcmd -S 127.0.0.1 -U sa -P 'YourStrong!Passw0rd' -d master -i scripts/local_db/sql/import_regions.sql

echo "END create_tables.sh [$(date)]"
