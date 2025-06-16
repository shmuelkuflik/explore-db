CREATE TABLE IF NOT EXISTS "Regions" (
    "Id" BIGINT PRIMARY KEY,
    "CloudIdInt" INTEGER NOT NULL,
    "RegionName" VARCHAR(64) NOT NULL,
    "RowVersion" INTEGER NOT NULL,
    "CreateTime" TIMESTAMP NOT NULL,
    "LastUpdateTime" TIMESTAMP NOT NULL,
    "FriendlyName" VARCHAR(128) NOT NULL,
    "FlagImageName" VARCHAR(128),
    "PublicAvailable" BOOLEAN NOT NULL DEFAULT FALSE,
    "CanCopyToOtherRegions" BOOLEAN NOT NULL DEFAULT FALSE
);
