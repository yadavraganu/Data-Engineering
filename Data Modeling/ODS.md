An Operational Data Store (ODS) is a module in the Data Warehouse that contains the most latest snapshot of Operational Data.  
It is designed to contain atomic or low-level data with limited history for “Real Time” or “Near Real Time” (NRT) reporting on frequent basis.
- An ODS is basically a database that is used for being an interim area for a data warehouse (DW), it sits between the legacy  
  systems environment and the DW.
- It works with a Data Warehouse (DW) but unlike a DW, an ODS does not contain Static data. Instead, an ODS contains data which is 
  dynamically and constantly updated through the various course of the Business Actions and Operations.  
- It is specifically designed so that it can Quickly perform simpler queries on smaller sets of data.  
- This is in contrast to the structure of DW wherein it needs to perform complex queries on large sets of data.  
- As the Data ages in ODS it passes out of the DW environment as it is.  
