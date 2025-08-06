# Library Data Model
## 1. Entities (Tables) and their Attributes
### **Member**
* `MemberID`: `VARCHAR(36)` (Primary Key, UUID)
* `FirstName`: `VARCHAR(50)`
* `LastName`: `VARCHAR(50)`
* `DateOfBirth`: `DATE`
* `Address`: `VARCHAR(255)`
* `PhoneNumber`: `VARCHAR(20)`
* `EmailAddress`: `VARCHAR(100)` (Unique)
* `RegistrationDate`: `DATE`
* `MembershipStatus`: `VARCHAR(20)` (e.g., 'Active', 'Suspended')
* `PasswordHash`: `VARCHAR(255)` (for online access)

### **Book**
* `BookID`: `VARCHAR(36)` (Primary Key, UUID for each *copy*)
* `ISBN`: `VARCHAR(17)` (Unique for each *title*, e.g., '978-3-16-148410-0')
* `Title`: `VARCHAR(255)`
* `Subtitle`: `VARCHAR(255)` (Optional)
* `PublicationYear`: `INT`
* `Edition`: `VARCHAR(50)` (Optional)
* `NumberOfPages`: `INT`
* `Description`: `TEXT` (Synopsis)
* `Language`: `VARCHAR(50)`
* `CoverImageUrl`: `VARCHAR(255)` (Optional)
* `AvailabilityStatus`: `VARCHAR(20)` (e.g., 'Available', 'On Loan', 'Reserved', 'Lost', 'Damaged')
* `LocationID`: `VARCHAR(36)` (Foreign Key to `Location`)

### **Author**
* `AuthorID`: `VARCHAR(36)` (Primary Key, UUID)
* `FirstName`: `VARCHAR(50)`
* `LastName`: `VARCHAR(50)`
* `DateOfBirth`: `DATE` (Optional)
* `Biography`: `TEXT` (Optional)

### **Publisher**
* `PublisherID`: `VARCHAR(36)` (Primary Key, UUID)
* `PublisherName`: `VARCHAR(100)` (Unique)
* `Address`: `VARCHAR(255)` (Optional)
* `PhoneNumber`: `VARCHAR(20)` (Optional)
* `Website`: `VARCHAR(255)` (Optional)

### **Genre**
* `GenreID`: `VARCHAR(36)` (Primary Key, UUID)
* `GenreName`: `VARCHAR(100)` (Unique, e.g., 'Fiction', 'Science Fiction')

### **Loan**
* `LoanID`: `VARCHAR(36)` (Primary Key, UUID)
* `BookID`: `VARCHAR(36)` (Foreign Key to `Book`)
* `MemberID`: `VARCHAR(36)` (Foreign Key to `Member`)
* `LoanDate`: `DATETIME`
* `ReturnDueDate`: `DATETIME`
* `ActualReturnDate`: `DATETIME` (NULL if not yet returned)
* `LoanStatus`: `VARCHAR(20)` (e.g., 'Active', 'Returned', 'Overdue')

### **Reservation**
* `ReservationID`: `VARCHAR(36)` (Primary Key, UUID)
* `BookID`: `VARCHAR(36)` (Foreign Key to `Book` - or `ISBN` if reserving a title)
* `MemberID`: `VARCHAR(36)` (Foreign Key to `Member`)
* `ReservationDate`: `DATETIME`
* `PickupExpiryDate`: `DATETIME` (When the reservation expires if not picked up)
* `ReservationStatus`: `VARCHAR(20)` (e.g., 'Pending', 'Ready for Pickup', 'Fulfilled', 'Expired', 'Canceled')

### **Staff**
* `StaffID`: `VARCHAR(36)` (Primary Key, UUID)
* `FirstName`: `VARCHAR(50)`
* `LastName`: `VARCHAR(50)`
* `EmailAddress`: `VARCHAR(100)` (Unique)
* `PhoneNumber`: `VARCHAR(20)` (Optional)
* `Role`: `VARCHAR(50)` (e.g., 'Librarian', 'Administrator', 'Clerk')
* `HireDate`: `DATE`
* `PasswordHash`: `VARCHAR(255)` (for system access)

### **Location**
* `LocationID`: `VARCHAR(36)` (Primary Key, UUID)
* `ShelfNumber`: `VARCHAR(50)`
* `AisleNumber`: `VARCHAR(50)`
* `Room`: `VARCHAR(100)` (e.g., 'Main Reading Room', 'Children\'s Section')
* `Description`: `VARCHAR(255)` (e.g., 'Non-fiction, History section')

### **Fine**
* `FineID`: `VARCHAR(36)` (Primary Key, UUID)
* `LoanID`: `VARCHAR(36)` (Foreign Key to `Loan`)
* `MemberID`: `VARCHAR(36)` (Foreign Key to `Member`)
* `FineAmount`: `DECIMAL(10, 2)`
* `FineDateIssued`: `DATETIME`
* `PaymentDate`: `DATETIME` (NULL if unpaid)
* `FineStatus`: `VARCHAR(20)` (e.g., 'Outstanding', 'Paid', 'Waived')
* `Reason`: `VARCHAR(255)` (e.g., 'Overdue', 'Damaged Book')

---

## 2. Junction Tables (for Many-to-Many Relationships)

### **BookAuthor**
* `BookID`: `VARCHAR(36)` (Primary Key, Foreign Key to `Book`)
* `AuthorID`: `VARCHAR(36)` (Primary Key, Foreign Key to `Author`)

### **BookGenre**
* `BookID`: `VARCHAR(36)` (Primary Key, Foreign Key to `Book`)
* `GenreID`: `VARCHAR(36)` (Primary Key, Foreign Key to `Genre`)

---

## 3. Relationships

* **Member** *to* **Loan**: One-to-Many
    * A `Member` can place many `Loan`s.
    * A `Loan` is placed by one `Member`.
* **Book** *to* **Loan**: One-to-Many
    * A `Book` copy can be part of many `Loan`s over time.
    * A `Loan` is for one specific `Book` copy.
* **Member** *to* **Reservation**: One-to-Many
    * A `Member` can make many `Reservation`s.
    * A `Reservation` is made by one `Member`.
* **Book** *to* **Reservation**: One-to-Many
    * A `Book` copy (or title) can be targeted by many `Reservation`s.
    * A `Reservation` targets one `Book` copy (or title).
* **Publisher** *to* **Book**: One-to-Many
    * A `Publisher` publishes many `Book`s.
    * A `Book` is published by one `Publisher`.
* **Location** *to* **Book**: One-to-Many
    * A `Location` can contain many `Book`s.
    * A `Book` is located at one `Location`.
* **Loan** *to* **Fine**: One-to-Many
    * A `Loan` can incur many `Fine`s (e.g., daily overdue fines).
    * A `Fine` is associated with one `Loan`.
* **Staff** *to* **Loan**: One-to-Many (Optional, if tracking which staff processed a loan)
    * A `Staff` member can process many `Loan`s.
    * A `Loan` is processed by one `Staff` member.
* **Staff** *to* **Fine**: One-to-Many (Optional, if tracking which staff issued a fine)
    * A `Staff` member can issue many `Fine`s.
    * A `Fine` is issued by one `Staff` member.
* **Book** *to* **Author**: Many-to-Many (via `BookAuthor` junction table)
    * A `Book` can have many `Author`s.
    * An `Author` can write many `Book`s.
* **Book** *to* **Genre**: Many-to-Many (via `BookGenre` junction table)
    * A `Book` can belong to many `Genre`s.
    * A `Genre` can classify many `Book`s.
<img width="1985" height="1398" alt="Library" src="https://github.com/user-attachments/assets/d1669457-b41e-48ea-beea-61eade8cd5a9" />
