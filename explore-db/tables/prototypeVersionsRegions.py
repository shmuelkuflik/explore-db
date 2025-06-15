from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PrototypeVersionsRegions(Base):
    __tablename__ = 'PrototypeVersionsRegions'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    PrototypeVersionId = Column(Integer, ForeignKey("PrototypeVersions.Id"), nullable=False)
    RegionId = Column(BigInteger, ForeignKey("Regions.Id"), nullable=False)
    LifecycleStatusInt = Column(Integer, nullable=False)
    ValidUntil = Column(DateTime, nullable=False)
    RowVersion = Column(Integer, nullable=False)
    CreateTime = Column(DateTime, nullable=False)
    LastUpdateTime = Column(DateTime, nullable=False)
    BackendPrototypeEnvId = Column(BigInteger, nullable=True)
    DeletionReasonInt = Column(Integer, nullable=True)
