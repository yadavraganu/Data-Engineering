# Types of Dimensions in Data Modeling

| Dimension Type              | Definition                                                                                   | Short Example                                                                                 |
|-----------------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Conformed                   | A single, consistent dimension reused by multiple fact tables to ensure uniform reporting.   | A `DimCustomer` table used by both `FactSales` and `FactSupport` to describe customers.       |
| Role-Playing                | One physical table that plays multiple roles in a fact via different foreign keys or aliases. | A `DimDate` table joined as `OrderDateKey` and `ShipDateKey` in the `FactSales` table.       |
| Slowly Changing (SCD)       | Tracks and preserves changes to dimension attributes over time using different versioning.    | A `DimProductPrice` that inserts a new row when a product’s price changes (Type 2).           |
| Junk                        | Combines low-cardinality flags or indicators into a single compact dimension table.          | A `DimOrderFlags` table consolidating `IsGift`, `IsReturn`, `IsExpress` into one code.       |
| Degenerate                  | Stores a business key or identifier directly in the fact table without a separate dimension. | The `InvoiceNumber` held in `FactTransactions` for drill-down, without a `DimInvoice` table.  |
| Outrigger                   | A secondary lookup table off a primary dimension, modeling an extra hierarchy or attributes. | A `DimProductCategory` table linked from `DimProduct` to hold category-level details.        |
| Shrunken (Shrunken)         | A rolled-up copy of a detailed dimension at a coarser grain for aggregate reporting.         | A `DimDateSummary` table listing only fiscal month, quarter, and year instead of every date. |
| Dimension-to-Dimension (Bridge) | A bridge table modeling many-to-many relationships or hierarchies between dimension members. | A `BridgeEmployeeManager` linking each employee to one or more managers over time.            |
| Swappable                   | Enables swapping between related dimensions dynamically at query time via a generic key.     | A `FactAttribution` that joins either `DimSalesRep` or `DimMarketingRep` based on a flag.     |
| Step                        | Captures process or workflow steps as attributes within one dimension to trace progress.      | A `DimOrderStep` listing timestamps for order received, processed, and shipped stages.        |

## Summary Comparison

| Dimension Type               | Purpose                                    | Example Dimension         |
|------------------------------|--------------------------------------------|---------------------------|
| Conformed                    | Shared across facts                        | DimCustomer               |
| Role-Playing                 | Multiple contextual joins                  | DimDate (Order/Ship)      |
| Slowly Changing (Type 1–3)   | Manage attribute history                   | DimProductPrice           |
| Junk                         | Consolidate flags/codes                    | DimOrderFlags             |
| Degenerate                   | Store identifiers in fact                  | InvoiceNumber in fact     |
| Outrigger                    | Secondary hierarchy off a primary dimension| DimProductCategory        |
| Shrunken                     | Coarser-grained copy of detailed dimension | DimDateSummary            |
| Dimension-to-Dimension       | Many-to-many or recursive hierarchies      | BridgeEmployeeManager     |
| Swappable                    | Dynamically swap attribution dimensions    | FactAttribution           |
| Step                         | Record discrete process steps              | DimOrderStep              |
