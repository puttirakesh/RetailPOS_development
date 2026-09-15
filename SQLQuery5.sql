SELECT TABLE_NAME, COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME IN (
    'IsDeleted', 'DeletedAt', 'IsActive', 'Status',
    'BranchId', 'CompanyId',
    'FinancialYear', 'FYCode', 'FinancialYearId',
    'RowVersion', 'Version', 'Timestamp'
)
AND TABLE_NAME LIKE 'RG_%'
ORDER BY TABLE_NAME, COLUMN_NAME;