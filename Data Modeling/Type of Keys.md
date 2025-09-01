### Type of Keys : 
- Super Keys
- Candidate Keys
- Primary Keys
- Alternate Keys
- Unique Key
- Composite Key
- Foreign Key

Employee Table Columns - {Id,Name,Ssn,Salary,Phone,Email}

### Super Keys
Super Key is defined as a set of attributes within a table that can uniquely identify each record within a table. Super Key is a superset of Candidate key.
- Attributes in super keys can have null values
  
E.g. : Id, Ssn, Email, (Name, Phone), (Id,Name), (Id,Ssn), (Ssn,Id) ...etc 

### Candidate Keys
Candidate keys are defined as the minimal set of fields which can uniquely identify each record in a table. 
It is an attribute or a set of attributes that can act as a Primary Key for a table to uniquely identify each record in that table. There can be more than one candidate key.
- A candiate key can never be NULL or empty. And its value should be unique.
- There can be more than one candidate keys for a table.
- A candidate key can be a combination of more than one columns(attributes).
  
E.g. : Id, Ssn, Email, (Name, Phone)

### Primary Keys
Primary key is a candidate key that is most appropriate to become the main key for any table.
- It is a key that can uniquely identify each record in a table.
- It cant have nulls
- There can be no room for duplicate rows when it comes to the case of Primary keys.
- Just one primary key can be used when working with the table.
- Primary keys can be formed from a single table or multiple fields of tables.
  
E.g. : Id

### Composite Keys
Key that consists of two or more attributes that uniquely identify any record in a table is called Composite key.
But the attributes which together form the Composite key are not a key independentely or individually

E.g. : (Name, Phone)

### Alternative Keys
The candidate key which are not selected as primary key are known as secondary keys or alternative keys.

E.g. : Ssn, Email, (Name, Phone)

### Foreign Keys
Foreign Key is used to establish relationships between two tables.
A foreign key will require each value in a column or set of columns to match the Primary Key of the referential table.
Foreign keys help to maintain data and referential integrity

### Unique Keys
Unique Key is a column or set of columns that uniquely identify each record in a table. All values will have to be unique in this Key.
A unique Key differs from a primary key because it can have only one null value, whereas a primary Key cannot have any null values.

E.g. : Email, (Name, Phone)
