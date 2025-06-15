from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = 'Regions'

    Id = Column(BigInteger, primary_key=True)
    CloudIdInt = Column(Integer, nullable=False)
    RegionName = Column(String(64), nullable=False)
    RowVersion = Column(Integer, nullable=False)
    CreateTime = Column(DateTime, nullable=False)
    LastUpdateTime = Column(DateTime, nullable=False)
    FriendlyName = Column(String(128), nullable=False)
    FlagImageName = Column(String(128))
    PublicAvailable = Column(Boolean, nullable=False, default=False)
    CanCopyToOtherRegions = Column(Boolean, nullable=False, default=False)
