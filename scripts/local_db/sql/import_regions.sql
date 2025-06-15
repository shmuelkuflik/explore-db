USE master;
GO

BULK INSERT Regions
FROM '/tmp/ITST_Test_1_dbo_Regions.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO
