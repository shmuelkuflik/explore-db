USE master;
GO

BULK INSERT $(FILE_NAME)
FROM "/tmp/$(FILE_NAME).csv"
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',  -- Unix LF
    TABLOCK,
    DATAFILETYPE = 'char'    -- Interprets the file as char, not native binary
);
GO
