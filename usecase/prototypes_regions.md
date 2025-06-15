# Prototypes and Regions

## query
```sql
select distinct p.Id as BlueprintId, r.RegionName
from [ITST].[dbo].Prototypes as p
inner join [ITST].[dbo].PrototypeVersions pv
on pv.PrototypeId = p.Id
inner join [ITST].[dbo].PrototypeVersionsRegions as pvr
on pvr.PrototypeVersionId = pv.Id
inner join [ITST].[dbo].Regions as r
on pvr.RegionId = r.Id
```
## connections
```
Prototypes(Id) -> PrototypeVersions(PrototypeId)
PrototypeVersions(Id) -> PrototypeVersionsRegions(PrototypeVersionId)
PrototypeVersionsRegions(RegionId) -> Regions(Id)
```
```
class Prototypes {
  + Id : int <<PK>> NOT NULL

class PrototypeVersions {
  + Id : int <<PK>> NOT NULL
  # PrototypeId : int <<FK>>, <<UK>> NOT NULL

class PrototypeVersionsRegions {
  # PrototypeVersionId : int <<FK>> NOT NULL
  # RegionId : bigint <<FK>> NOT NULL

class Regions {
  + Id : bigint <<PK>> NOT NULL
    RegionName : nvarchar NOT NULL
```
## inspections
Regions table was last updated on 2016

| Region            | Last Updated           |
|-------------------|------------------------|
| Miami             | 2014-11-30 05:56:28.057 |
| us-east-1         | 2014-11-30 05:56:28.057 |
| eu-west-1         | 2014-11-30 05:56:28.057 |
| ap-southeast-2    | 2014-12-14 06:48:44.893 |
| us-west-1         | 2014-12-14 06:48:44.893 |
| ap-southeast-1    | 2016-02-23 00:00:00.000 |
| VMware_Singapore  | 2016-06-23 00:00:00.000 |
| VMware_Amsterdam  | 2016-06-23 00:00:00.000 |