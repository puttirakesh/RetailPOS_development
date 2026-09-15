SELECT 
    t.name AS TableName,
    i.name AS IndexName,
    i.is_unique,
    i.is_primary_key,
    STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS Columns
FROM sys.tables t
JOIN sys.indexes i ON t.object_id = i.object_id
JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE t.name LIKE 'RG_%'
GROUP BY t.name, i.name, i.is_unique, i.is_primary_key
ORDER BY t.name, i.is_primary_key DESC, i.name;