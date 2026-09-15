SELECT 
    c.TABLE_NAME,
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.NUMERIC_PRECISION,
    c.NUMERIC_SCALE,
    c.IS_NULLABLE,
    COLUMNPROPERTY(OBJECT_ID(c.TABLE_SCHEMA + '.' + c.TABLE_NAME), c.COLUMN_NAME, 'IsIdentity') AS IsIdentity,
    c.COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_NAME IN (
    'RG_Brand', 'RG_Category', 'RG_Group', 'RG_Mark', 'RG_Attribute',
    'RG_UOM', 'RG_TaxMaster', 'RG_Slab', 'RG_State', 'RG_City',
    'RG_Customer', 'RG_Supplier', 'RG_Agent', 'RG_Purchaser', 'RG_SalesPerson',
    'RG_Product', 'RG_Branch', 'RG_User', 'RG_FinancialYear'
    -- add any other tables that appear in the first query that look important
)
ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;