from dal_mssql import MssqlDal
from regions import Region

if __name__ == "__main__":
    mssqlDal = MssqlDal()
    mssqlDal.db_query()

    regions = mssqlDal.session.query(Region).all()

    for region in regions:
        print(f"{region.Id}: {region.FriendlyName} - {region.RegionName}")

    mssqlDal.session.close()
    print("END")