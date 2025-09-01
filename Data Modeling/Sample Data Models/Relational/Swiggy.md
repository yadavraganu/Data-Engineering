# Swiggy Data Model - Detailed ER Diagram Representation
## I. Core Entities

### 1. User
* `user_id` (Primary Key - PK)
* `name`
* `email`
* `phone_number`
* `password_hash`
* `registration_date`
* `account_status` (e.g., 'active', 'inactive', 'blocked')
* `loyalty_points`
* `preferred_cuisine` (for recommendations)

### 2. Address
* `address_id` (PK)
* `user_id` (Foreign Key - FK to User.user_id)
* `street_address`
* `apartment_details`
* `landmark`
* `city`
* `state`
* `pincode` (zip/postal code)
* `latitude`
* `longitude`
* `address_type` (e.g., 'home', 'work', 'other')
* `is_default` (boolean)

### 3. Delivery_Partner
* `delivery_partner_id` (PK)
* `user_id` (FK to User.user_id, if Delivery Partner is a type of User)
* `name`
* `phone_number`
* `vehicle_type` (e.g., 'bike', 'scooter', 'cycle')
* `vehicle_model`
* `license_plate`
* `driver_license_info`
* `bank_account_details` (for payouts)
* `rating` (average rating from customers and restaurants)
* `status` (e.g., 'online', 'offline', 'on_delivery', 'available')
* `current_location_latitude` (volatile, often separate real-time store)
* `current_location_longitude` (volatile, often separate real-time store)
* `delivery_count` (total deliveries completed)

### 4. Restaurant
* `restaurant_id` (PK)
* `name`
* `address` (full string, or separate Address entity for restaurants)
* `latitude`
* `longitude`
* `phone_number`
* `email`
* `cuisine_types` (array/list of strings)
* `rating` (average rating from customers)
* `total_ratings`
* `average_delivery_time`
* `status` (e.g., 'open', 'closed', 'on_holiday', 'temporarily_unavailable')
* `opening_hours` (JSON/Text for daily hours)
* `fssai_license_info`
* `gst_info`
* `commission_rate` (negotiated with Swiggy)

### 5. Menu
* `menu_id` (PK)
* `restaurant_id` (FK to Restaurant.restaurant_id)
* `menu_name` (e.g., 'Main Menu', 'Breakfast Menu', 'Seasonal Specials')
* `is_active` (boolean)
* `last_updated`

### 6. Menu_Item
* `item_id` (PK)
* `menu_id` (FK to Menu.menu_id)
* `name` (e.g., 'Butter Chicken', 'Paneer Tikka Masala')
* `description`
* `price`
* `image_url`
* `category` (e.g., 'Appetizers', 'Main Course', 'Desserts', 'Beverages')
* `is_vegetarian` (boolean)
* `is_available` (boolean - for real-time stock management)
* `customization_options` (JSON/Text for options like 'spice level', 'add-ons')
* `allergens` (array/list of strings)

### 7. Order
* `order_id` (PK)
* `user_id` (FK to User.user_id)
* `restaurant_id` (FK to Restaurant.restaurant_id)
* `delivery_partner_id` (FK to Delivery_Partner.delivery_partner_id, Nullable until assigned)
* `delivery_address_id` (FK to Address.address_id)
* `order_time` (timestamp when placed)
* `pickup_time` (timestamp when food picked up by DP)
* `delivery_time` (timestamp when food delivered)
* `estimated_delivery_time`
* `total_amount`
* `discount_amount`
* `delivery_fee`
* `packaging_fee`
* `taxes`
* `final_amount` (after all deductions/additions)
* `order_status` (e.g., 'placed', 'confirmed', 'preparing', 'picked_up', 'out_for_delivery', 'delivered', 'cancelled', 'refunded')
* `instructions_to_restaurant`
* `instructions_to_delivery_partner`

### 8. Order_Item
* `order_item_id` (PK)
* `order_id` (FK to Order.order_id)
* `item_id` (FK to Menu_Item.item_id)
* `quantity`
* `price_at_order_time`
* `customizations_selected` (JSON of selected options and their prices)
* `special_requests` (e.g., "no onions")

### 9. Payment
* `payment_id` (PK)
* `order_id` (FK to Order.order_id)
* `user_id` (FK to User.user_id)
* `amount`
* `currency`
* `payment_method_type` (e.g., 'credit_card', 'UPI', 'cash_on_delivery', 'digital_wallet')
* `transaction_status` (e.g., 'pending', 'successful', 'failed', 'refunded')
* `transaction_timestamp`
* `payment_gateway_reference` (e.g., Stripe, Razorpay transaction ID)

### 10. Rating_Review
* `review_id` (PK)
* `order_id` (FK to Order.order_id)
* `user_id` (FK to User.user_id - the reviewer)
* `restaurant_id` (FK to Restaurant.restaurant_id, Nullable)
* `delivery_partner_id` (FK to Delivery_Partner.delivery_partner_id, Nullable)
* `rating_value` (e.g., 1-5 stars)
* `comment` (text feedback)
* `timestamp`
* `is_anonymous` (boolean)

## II. Relationships

This section describes the relationships between the entities. Cardinality is indicated as (Source Entity Cardinality) -- Relationship -- (Target Entity Cardinality).

* **User** (1) -- `HAS` -- (M) **Address**
    * *(FK: `Address.user_id`)*
* **User** (1) -- `CAN_BE` -- (0 or 1) **Delivery_Partner**
    * *(FK: `Delivery_Partner.user_id`, if delivery partners are a subset of users)*
* **Restaurant** (1) -- `HAS` -- (M) **Menu**
    * *(FK: `Menu.restaurant_id`)*
* **Menu** (1) -- `CONTAINS` -- (M) **Menu_Item**
    * *(FK: `Menu_Item.menu_id`)*
* **User** (1) -- `PLACES` -- (M) **Order**
    * *(FK: `Order.user_id`)*
* **Restaurant** (1) -- `RECEIVES` -- (M) **Order**
    * *(FK: `Order.restaurant_id`)*
* **Delivery_Partner** (0 or 1) -- `FULFILLS` -- (M) **Order**
    * *(FK: `Order.delivery_partner_id`)*
* **Address** (1) -- `IS_DELIVERY_TO` -- (M) **Order**
    * *(FK: `Order.delivery_address_id`)*
* **Order** (1) -- `COMPRISES` -- (M) **Order_Item**
    * *(FK: `Order_Item.order_id`)*
* **Menu_Item** (1) -- `IS_PART_OF` -- (M) **Order_Item**
    * *(FK: `Order_Item.item_id`)*
* **Order** (1) -- `INVOLVES` -- (1) **Payment**
    * *(FK: `Payment.order_id`)*
* **User** (1) -- `INITIATES` -- (M) **Rating_Review**
    * *(FK: `Rating_Review.user_id`)*
* **Order** (1) -- `IS_RATED_ON` -- (M) **Rating_Review**
    * *(FK: `Rating_Review.order_id`)*
* **Restaurant** (1) -- `RECEIVES` -- (M) **Rating_Review**
    * *(FK: `Rating_Review.restaurant_id`)*
* **Delivery_Partner** (1) -- `RECEIVES` -- (M) **Rating_Review**
    * *(FK: `Rating_Review.delivery_partner_id`)*

## III. Additional Considerations

* **Polyglot Persistence:** Swiggy likely uses a mix of relational (PostgreSQL, MySQL for transactional data), NoSQL (MongoDB, Cassandra for flexible schemas), in-memory (Redis for caching/real-time locations), and big data technologies (Kafka, Spark for analytics and event streaming).
* **Microservices Architecture:** Each entity or closely related group of entities would typically be managed by a dedicated microservice, potentially having its own optimized data store.
* **Real-time Data:** Live location tracking for delivery partners and order status updates are handled by highly optimized, often in-memory or stream-processing systems.
* **Scalability:** Extensive use of sharding, replication, and distributed databases to handle massive user and order volumes.
<img width="2362" height="3840" alt="Swiggy" src="https://github.com/user-attachments/assets/45d573d7-a9e7-4a73-9597-1c49dcca9d9e" />
