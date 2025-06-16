CREATE TABLE IF NOT EXISTS "PrototypeVersions" (
    "Id" SERIAL PRIMARY KEY
--    "PrototypeId" INTEGER NOT NULL REFERENCES "Prototypes"("Id"),
--    "Version_Number" INTEGER NOT NULL,
--    "Version_Name" VARCHAR(32) NOT NULL,
--    "Version_Comment" TEXT,
--    "BackendPrototypeEnvId" BIGINT REFERENCES "BackendPrototypeEnvs"("Id"),
--    "RowVersion" INTEGER NOT NULL,
--    "CreateTime" TIMESTAMP NOT NULL,
--    "LastUpdateTime" TIMESTAMP NOT NULL,
--    "Version_AuthorId" INTEGER NOT NULL REFERENCES "Users"("Id"),
--    "ParentPrototypeVersionForUiId" INTEGER REFERENCES "PrototypeVersions"("Id"),
--    "ParentPrototypeVersionForMachinesId" INTEGER REFERENCES "PrototypeVersions"("Id"),
--    "CreationOriginatorInt" INTEGER,
--    "CopyOperationInt" INTEGER NOT NULL,
--    "CreatedByEnvId" BIGINT REFERENCES "Envs"("Id"),
--    "Resources_DiskSizeMB" BIGINT,
--    "Resources_CpuCount" INTEGER,
--    "Resources_MemorySizeMB" BIGINT,
--    "ValidUntil" TIMESTAMP,
--    "VixLoginFailureReason" VARCHAR(300),
--    "Metadata_Name" VARCHAR(100) NOT NULL,
--    "Metadata_Description" TEXT,
--    "Metadata_ImageName" VARCHAR(128),
--    "Metadata_EnvExplorerXml" TEXT,
--    "Metadata_CleanDescription" TEXT,
--    "ExternalSystemId" VARCHAR(128),
--    "ViewerCustomizationId" BIGINT,
--    "Metadata_EnableRdp10ForPublicCloudVms" BOOLEAN,
--    CONSTRAINT "UQ_PrototypeVersions_BIZKEY" UNIQUE ("PrototypeId", "Version_Number")
);

--CREATE INDEX "IX_PrototypeVersions_ViewerCustomizationId"
--    ON "PrototypeVersions" ("ViewerCustomizationId");
--
--CREATE INDEX "IX_CreateTime_ValidUntil"
--    ON "PrototypeVersions" ("CreateTime", "ValidUntil")
--    INCLUDE ("PrototypeId", "Resources_DiskSizeMB", "Resources_CpuCount", "Resources_MemorySizeMB")
--    WHERE "ValidUntil" IS NOT NULL;