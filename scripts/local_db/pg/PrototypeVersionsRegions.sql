CREATE TABLE IF NOT EXISTS "PrototypeVersionsRegions" (
    "Id" SERIAL PRIMARY KEY,
    "PrototypeVersionId" INT NOT NULL REFERENCES "PrototypeVersions"("Id"),
    "RegionId" BIGINT NOT NULL REFERENCES "Regions"("Id"),
    "LifecycleStatusInt" INT NOT NULL,
    "ValidUntil" TIMESTAMP NOT NULL,
    "RowVersion" INT NOT NULL,
    "CreateTime" TIMESTAMP NOT NULL,
    "LastUpdateTime" TIMESTAMP NOT NULL,
    "BackendPrototypeEnvId" BIGINT REFERENCES "BackendPrototypeEnvs"("Id"),
    "DeletionReasonInt" INT
);

CREATE UNIQUE INDEX IF NOT EXISTS "UQ_PrototypeVersionsRegions_BIZKEY"
    ON "PrototypeVersionsRegions" ("PrototypeVersionId", "RegionId", "ValidUntil");

CREATE INDEX IF NOT EXISTS "IX_LifecycleStatusInt"
    ON "PrototypeVersionsRegions" ("LifecycleStatusInt", "PrototypeVersionId");
