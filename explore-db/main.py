from dal_mssql import MssqlDal
from tables.regions import Region
from tables.prototypeVersionsRegions import PrototypeVersionsRegions

if __name__ == "__main__":
    mssqlDal = MssqlDal()
    mssqlDal.db_query()

    print("---- Regions ----")
    regions = mssqlDal.session.query(Region).all()
    for region in regions:
        print(f"{region.Id}: {region.FriendlyName} - {region.RegionName}")

    print("---- PrototypeVersionsRegions ----")
    rows = mssqlDal.session.query(PrototypeVersionsRegions).filter(PrototypeVersionsRegions.RegionId != 0).limit(10).all()
    for row in rows:
        print(row.Id, row.RegionId)

    print("---- Join Regions and PrototypeVersionsRegions ----")
    rows = (
        mssqlDal.session.query(Region, PrototypeVersionsRegions)
            .join(PrototypeVersionsRegions, Region.Id == PrototypeVersionsRegions.RegionId)
            .filter(PrototypeVersionsRegions.RegionId != 0)
            .order_by(Region.Id)
            .limit(10)
            .all()
    )
    for region, prototype_version_region in rows:
        print(f"Region: {region.Id} - {region.FriendlyName}, PrototypeVersionRegion: {prototype_version_region.Id} - {prototype_version_region.PrototypeVersionId}")

    mssqlDal.session.close()
    print("END")