USE master;
GO

CREATE TABLE Regions (
    Id                    BIGINT NOT NULL PRIMARY KEY,
    CloudIdInt            INT NOT NULL,
    RegionName            NVARCHAR(64) NOT NULL,
    RowVersion            INT NOT NULL,
    CreateTime            DATETIME NOT NULL,
    LastUpdateTime        DATETIME NOT NULL,
    FriendlyName          NVARCHAR(128) NOT NULL,
    FlagImageName         NVARCHAR(128),
    PublicAvailable       BIT NOT NULL DEFAULT 0,
    CanCopyToOtherRegions BIT NOT NULL DEFAULT 0
);
