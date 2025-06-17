SELECT
    tp.name AS PARENT_TABLE,
    tr.name AS REFERENCED_TABLE
FROM sys.foreign_keys fk
INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
WHERE SCHEMA_NAME(tp.schema_id) = 'dbo';