USE master;
GO

-- Minimal definitions of the referenced tables so foreign keys work
IF OBJECT_ID('dbo.PrototypeVersions', 'U') IS NULL
CREATE TABLE dbo.PrototypeVersions (
    Id INT PRIMARY KEY
);
GO

IF OBJECT_ID('dbo.Regions', 'U') IS NULL
CREATE TABLE dbo.Regions (
    Id BIGINT PRIMARY KEY
);
GO

IF OBJECT_ID('dbo.BackendPrototypeEnvs', 'U') IS NULL
CREATE TABLE dbo.BackendPrototypeEnvs (
    Id BIGINT PRIMARY KEY
);
GO

-- Now create the actual table with FKs
CREATE TABLE dbo.PrototypeVersionsRegions
(
    Id                    INT IDENTITY
        CONSTRAINT PK_PrototypeVersionsRegions
            PRIMARY KEY
                WITH (FILLFACTOR = 80),
    PrototypeVersionId    INT      NOT NULL
        CONSTRAINT FK_PrototypeVersions_PrototypesVersionsRegions_PrototypeVersionId
            REFERENCES dbo.PrototypeVersions(Id),
    RegionId              BIGINT   NOT NULL
        CONSTRAINT FK_Regions_PrototypesVersionsRegions_RegionId
            REFERENCES dbo.Regions(Id),
    LifecycleStatusInt    INT      NOT NULL,
    ValidUntil            DATETIME NOT NULL,
    RowVersion            INT      NOT NULL,
    CreateTime            DATETIME NOT NULL,
    LastUpdateTime        DATETIME NOT NULL,
    BackendPrototypeEnvId BIGINT
        CONSTRAINT FK_BackendPrototypeEnvs_PrototypeVersionsRegions_BackendPrototypeEnvId
            REFERENCES dbo.BackendPrototypeEnvs(Id),
    DeletionReasonInt     INT
);
GO

CREATE UNIQUE INDEX UQ_PrototypeVersionsRegions_BIZKEY
    ON dbo.PrototypeVersionsRegions (PrototypeVersionId, RegionId, ValidUntil)
    WITH (FILLFACTOR = 100);
GO

CREATE INDEX IX_LifecycleStatusInt
    ON dbo.PrototypeVersionsRegions (LifecycleStatusInt, PrototypeVersionId)
    WITH (FILLFACTOR = 100);
GO
