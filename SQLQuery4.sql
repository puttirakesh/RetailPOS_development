SELECT 
    fk.name AS FK_Name,
    OBJECT_NAME(fk.parent_object_id) AS ParentTable,
    COL_NAME(fc.parent_object_id, fc.parent_column_id) AS ParentColumn,
    OBJECT_NAME(fk.referenced_object_id) AS ReferencedTable,
    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS ReferencedColumn
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fc ON fk.object_id = fc.constraint_object_id
WHERE OBJECT_NAME(fk.parent_object_id) LIKE 'RG_%'
ORDER BY ParentTable, FK_Name;