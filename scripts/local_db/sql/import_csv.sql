USE master;
GO

BULK INSERT PrototypeVersionsRegions
FROM "/tmp/$(FILE_NAME).csv"
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',  -- Unix LF
    TABLOCK,
    DATAFILETYPE = 'char'    -- Interprets the file as char, not native binary
);
GO

\copy PrototypeVersionsRegions FROM '/tmp/PrototypeVersionsRegions.csv' WITH (
    FORMAT csv,
    HEADER,
    DELIMITER ',',
    NULL '',
    QUOTE '"'
);
