## E-commerce Platform ER Model
### Entities and Their Attributes:
#### 1. **User**
* **Description:** Represents a registered user of the platform.
* **Attributes:**
  * `user_id` (Primary Key)
  * `username` (Unique)
  * `email` (Unique)
  * `password_hash`
  * `first_name`
  * `last_name`
  * `phone_number`
  * `registration_date`
  * `last_login`
  * `is_admin` (Boolean)
#### 2. **Product**
* **Description:** Represents an item available for sale.
* **Attributes:**
  * `product_id` (Primary Key)
  * `name`
  * `description`
  * `price` (Decimal)
  * `stock_quantity` (Integer)
  * `category_id` (Foreign Key to Category)
  * `brand_id` (Foreign Key to Brand)
  * `image_url`
  * `weight` (Decimal, optional)
  * `dimensions` (String, optional)
  * `created_at`
  * `updated_at`
  * `is_available` (Boolean)
#### 3. **Category**
* **Description:** Groups similar products.
* **Attributes:**
  * `category_id` (Primary Key)
  * `name` (Unique)
  * `description`
  * `parent_category_id` (Self-referencing Foreign Key for subcategories, optional)
#### 4. **Brand**
* **Description:** The manufacturer or brand of a product.
* **Attributes:**
  * `brand_id` (Primary Key)
  * `name` (Unique)
  * `description`
  * `logo_url`
#### 5. **Order**
* **Description:** A transaction initiated by a user to purchase products.
* **Attributes:**
  * `order_id` (Primary Key)
  * `user_id` (Foreign Key to User)
  * `order_date`
  * `total_amount` (Decimal)
  * `status` (e.g., 'Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled')
  * `shipping_address_id` (Foreign Key to Address)
  * `billing_address_id` (Foreign Key to Address)
  * `payment_method`
  * `transaction_id` (Unique, from payment gateway)
#### 6. **OrderItem**
* **Description:** Represents a specific product within an order.
* **Attributes:**
  * `order_item_id` (Primary Key)
  * `order_id` (Foreign Key to Order)
  * `product_id` (Foreign Key to Product)
  * `quantity` (Integer)
  * `price_at_time_of_order` (Decimal)
#### 7. **Address**
* **Description:** Stores address details for users (shipping, billing).
* **Attributes:**
  * `address_id` (Primary Key)
  * `user_id` (Foreign Key to User)
  * `address_line1`
  * `address_line2` (Optional)
  * `city`
  * `state_province`
  * `postal_code`
  * `country`
  * `address_type` (e.g., 'Shipping', 'Billing', 'Both')
#### 8. **Cart**
* **Description:** Represents a user's shopping cart for active purchases.
* **Attributes:**
  * `cart_id` (Primary Key)
  * `user_id` (Foreign Key to User, Unique)
  * `created_at`
  * `updated_at`
#### 9. **CartItem**
* **Description:** Represents a product in a user's shopping cart.
* **Attributes:**
  * `cart_item_id` (Primary Key)
  * `cart_id` (Foreign Key to Cart)
  * `product_id` (Foreign Key to Product)
  * `quantity` (Integer)
  * `added_date`
#### 10. **Review**
* **Description:** User-generated reviews for products.
* **Attributes:**
  * `review_id` (Primary Key)
  * `user_id` (Foreign Key to User)
  * `product_id` (Foreign Key to Product)
  * `rating` (Integer, e.g., 1-5)
  * `comment` (Text)
  * `review_date`
#### 11. **Payment**
* **Description:** Records payment details for an order.
* **Attributes:**
  * `payment_id` (Primary Key)
  * `order_id` (Foreign Key to Order)
  * `payment_date`
  * `amount` (Decimal)
  * `payment_method` (e.g., 'Credit Card', 'PayPal', 'Net Banking')
  * `status` (e.g., 'Completed', 'Failed', 'Refunded')
  * `transaction_id` (Unique, from payment gateway)
#### 12. **Wishlist** (Optional)
* **Description:** A list of products a user desires to purchase later.
* **Attributes:**
  * `wishlist_id` (Primary Key)
  * `user_id` (Foreign Key to User, Unique)
  * `created_at`
#### 13. **WishlistItem** (Optional)
* **Description:** A product in a user's wishlist.
* **Attributes:**
  * `wishlist_item_id` (Primary Key)
  * `wishlist_id` (Foreign Key to Wishlist)
  * `product_id` (Foreign Key to Product)
  * `added_date`
### Relationships:
Here, we'll describe the relationships between entities, including cardinality (one-to-one, one-to-many, many-to-many).
* **User --- (1:N) ---> Address**
  * A **User** can have multiple **Address**es (shipping, billing).
  * An **Address** belongs to one **User**.
* **User --- (1:N) ---> Order**
  * A **User** can place multiple **Order**s.
  * An **Order** is placed by one **User**.
* **User --- (1:1) ---> Cart**
  * A **User** has one **Cart**.
  * A **Cart** belongs to one **User**.
* **User --- (1:N) ---> Review**
  * A **User** can write multiple **Review**s.
  * A **Review** is written by one **User**.
* **User --- (1:1) ---> Wishlist** (Optional)
  * A **User** has one **Wishlist**.
  * A **Wishlist** belongs to one **User**.
* **Product --- (1:N) ---> OrderItem**
  * A **Product** can be part of many **OrderItem**s.
  * An **OrderItem** refers to one **Product**.
* **Product --- (1:N) ---> CartItem**
  * A **Product** can be in many **CartItem**s.
  * A **CartItem** refers to one **Product**.
* **Product --- (1:N) ---> Review**
  * A **Product** can have multiple **Review**s.
  * A **Review** is for one **Product**.
* **Product --- (1:N) ---> WishlistItem** (Optional)
  * A **Product** can be in many **WishlistItem**s.
  * A **WishlistItem** refers to one **Product**.
* **Category --- (1:N) ---> Product**
  * A **Category** can contain multiple **Product**s.
  * A **Product** belongs to one **Category**.
* **Brand --- (1:N) ---> Product**
  * A **Brand** can have multiple **Product**s.
  * A **Product** belongs to one **Brand**.
* **Order --- (1:N) ---> OrderItem**
  * An **Order** can contain multiple **OrderItem**s.
  * An **OrderItem** belongs to one **Order**.
* **Order --- (1:N) ---> Payment**
  * An **Order** can have multiple **Payment**s (e.g., initial payment, refunds).
  * A **Payment** is for one **Order**.
* **Cart --- (1:N) ---> CartItem**
  * A **Cart** can contain multiple **CartItem**s.
  * A **CartItem** belongs to one **Cart**.
* **Wishlist --- (1:N) ---> WishlistItem** (Optional)
  * A **Wishlist** can contain multiple **WishlistItem**s.
  * A **WishlistItem** belongs to one **Wishlist**.
* **Address --- (1:N) ---> Order** (through `shipping_address_id` and `billing_address_id`)
  * An **Address** can be used for multiple **Order**s (as shipping or billing address).

  * An **Order** uses two **Address**es (one shipping, one billing).
<img width="6384" height="4140" alt="image" src="https://github.com/user-attachments/assets/ee5bc699-3ab4-4002-a8c2-419fa0c64a25" />
