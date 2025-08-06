# Netflix Core Data Model: Entity-Relationship Diagram
**1. Entity: `Users`**
* **Attributes:**
  * `user_id` (Primary Key, Unique Identifier)
  * `email` (Unique)
  * `name`
  * `password_hash`
  * `registration_date`
  * `location`
    
**2. Entity: `Profiles`**
* **Attributes:**
  * `profile_id` (Primary Key, Unique Identifier)
  * `profile_name`
  * `profile_type` (e.g., 'adult', 'kid')
  * `avatar_url`
* **Relationships:**
  * **`Users` to `Profiles`:** One-to-Many
    * A `User` can have one or more `Profiles`.
    * Each `Profile` belongs to exactly one `User`.
    * (Relationship: `has_profiles`)
    * `user_id` (Foreign Key from `Users`)

**3. Entity: `Content`**
* **Attributes:**
  * `content_id` (Primary Key, Unique Identifier)
  * `title`
  * `description`
  * `release_year`
  * `rating` (e.g., 'TV-MA', 'PG-13')
  * `duration_minutes`
  * `language`
  * `thumbnail_url`
  * `video_url` (simplified; in reality, multiple versions/CDN links)
    
**4. Entity: `Genres`**
* **Attributes:**
  * `genre_id` (Primary Key, Unique Identifier)
  * `genre_name` (e.g., 'Action', 'Drama', 'Comedy')
* **Relationships:**
  * **`Content` to `Genres`:** Many-to-Many (via `Content_Genres` join table)
    * A `Content` item can belong to multiple `Genres`.
    * A `Genre` can be associated with multiple `Content` items.
      
**5. Entity: `Content_Genres` (Join Table)**
* **Attributes:**
  * `content_id` (Foreign Key from `Content`, Part of Composite Primary Key)
  * `genre_id` (Foreign Key from `Genres`, Part of Composite Primary Key)
    
**6. Entity: `Actors`**
* **Attributes:**
  * `actor_id` (Primary Key, Unique Identifier)
  * `actor_name`
  * `birthdate`
  * `biography`
* **Relationships:**
  * **`Content` to `Actors`:** Many-to-Many (via `Content_Cast` join table)
    * A `Content` item can feature multiple `Actors`.
    * An `Actor` can appear in multiple `Content` items.
      
**7. Entity: `Content_Cast` (Join Table)**
* **Attributes:**
  * `content_id` (Foreign Key from `Content`, Part of Composite Primary Key)
  * `actor_id` (Foreign Key from `Actors`, Part of Composite Primary Key)
  * `role_name` (e.g., 'Protagonist, Supporting Character')
    
**8. Entity: `Viewing_History`**
* **Attributes:**
  * `history_id` (Primary Key, Unique Identifier)
  * `watched_at` (Timestamp of last watch)
  * `current_playback_position_seconds`
  * `is_completed` (Boolean)
* **Relationships:**
  * **`Profiles` to `Viewing_History`:** One-to-Many
    * A `Profile` can have many `Viewing_History` records.
    * Each `Viewing_History` record belongs to one `Profile`.
    * `profile_id` (Foreign Key from `Profiles`)
  * **`Content` to `Viewing_History`:** One-to-Many
    * A `Content` item can appear in many `Viewing_History` records.
    * Each `Viewing_History` record is for one `Content` item.
    * `content_id` (Foreign Key from `Content`)
      
**9. Entity: `Ratings`**
* **Attributes:**
  * `rating_id` (Primary Key, Unique Identifier)
  * `rating_value` (e.g., 'thumbs_up', 'thumbs_down', or a numerical scale)
  * `rating_date`
* **Relationships:**
  * **`Profiles` to `Ratings`:** One-to-Many
    * A `Profile` can give many `Ratings`.
    * Each `Rating` is given by one `Profile`.
    * `profile_id` (Foreign Key from `Profiles`)
  * **`Content` to `Ratings`:** One-to-Many
    * A `Content` item can receive many `Ratings`.
    * Each `Rating` is for one `Content` item.
    * `content_id` (Foreign Key from `Content`)
      
**10. Entity: `Subscription_Plans`**
* **Attributes:**
  * `plan_id` (Primary Key, Unique Identifier)
  * `plan_name` (e.g., 'Basic', 'Standard', 'Premium')
  * `monthly_price`
  * `max_screens`
  * `video_quality` (e.g., 'SD', 'HD', '4K')
    
**11. Entity: `Subscriptions`**
* **Attributes:**
  * `subscription_id` (Primary Key, Unique Identifier)
  * `start_date`
  * `end_date`
  * `status` (e.g., 'Active', 'Cancelled', 'Expired')
* **Relationships:**
  * **`Users` to `Subscriptions`:** One-to-Many
    * A `User` can have one or more `Subscriptions` (historically or concurrently if allowed).
    * Each `Subscription` belongs to one `User`.
    * `user_id` (Foreign Key from `Users`)
  * **`Subscription_Plans` to `Subscriptions`:** One-to-Many
    * A `Subscription_Plan` can be chosen by many `Subscriptions`.
    * Each `Subscription` is based on one `Subscription_Plan`.
    * `plan_id` (Foreign Key from `Subscription_Plans`)
      
**Summary of Relationships and Cardinalities:**
* `Users` (1) -- `has_profiles` -- (M) `Profiles`
* `Profiles` (1) -- `watches` -- (M) `Viewing_History`
* `Content` (1) -- `is_watched_in` -- (M) `Viewing_History`
* `Profiles` (1) -- `rates` -- (M) `Ratings`
* `Content` (1) -- `is_rated_by` -- (M) `Ratings`
* `Content` (M) -- `has_genres` -- (M) `Genres` (via `Content_Genres` join table)
* `Content` (M) -- `features_actors` -- (M) `Actors` (via `Content_Cast` join table)
* `Users` (1) -- `has_subscriptions` -- (M) `Subscriptions`
* `Subscription_Plans` (1) -- `chosen_by` -- (M) `Subscriptions`

<img width="3840" height="3720" alt="Untitled diagram _ Mermaid Chart-2025-07-13-023709" src="https://github.com/user-attachments/assets/f8948fe4-13c7-4d9f-961d-e7d481dc7502" />
