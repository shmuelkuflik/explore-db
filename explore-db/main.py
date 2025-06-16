from dal_mssql import MssqlDal
from dal_pg import PostgressDal
from tables.prototypeVersionsRegions import PrototypeVersionsRegions
from tables.regions import Region


def query_regions(dal):
    global region
    regions = dal.session.query(Region).all()
    for region in regions:
        print(f"{region.Id}: {region.FriendlyName} - {region.RegionName}")


def query_PrototypeVersionsRegions(dal):
    global rows
    rows = dal.session.query(PrototypeVersionsRegions).filter(
        PrototypeVersionsRegions.PrototypeVersionId > 2000).limit(10).all()
    for row in rows:
        print(row.Id, row.PrototypeVersionId)


def run_join(dal):
    global rows, region
    rows = (
        dal.session.query(Region, PrototypeVersionsRegions)
        .join(PrototypeVersionsRegions, Region.Id == PrototypeVersionsRegions.RegionId)
        .filter(PrototypeVersionsRegions.PrototypeVersionId > 2000)
        .order_by(Region.Id)
        .limit(10)
        .all()
    )
    for region, prototype_version_region in rows:
        print(
            f"Region: {region.Id} - {region.FriendlyName}, PrototypeVersionRegion: {prototype_version_region.Id} - {prototype_version_region.PrototypeVersionId}")


if __name__ == "__main__":
    dal_pg = PostgressDal()
    dal_sql = MssqlDal()

    dal_sql.db_query()

    print("---- Regions: sql ----")
    query_regions(dal_sql)
    print("---- Regions: pg ----")
    query_regions(dal_pg)

    print("---- PrototypeVersionsRegions: sql ----")
    query_PrototypeVersionsRegions(dal_sql)
    print("---- PrototypeVersionsRegions: pg ----")
    query_PrototypeVersionsRegions(dal_pg)

    print("---- Join Regions and PrototypeVersionsRegions: sql ----")
    run_join(dal_sql)
    print("---- Join Regions and PrototypeVersionsRegions: pg ----")
    run_join(dal_pg)

    dal_sql.session.close()
    dal_pg.session.close()
    print("END")