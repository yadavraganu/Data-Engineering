# Netflix Dimensional Model

Below is a dimensional model for a Netflix-like analytics platform. It consists of a central fact table capturing viewing events and surrounding dimension tables that provide rich context for each event.

## Fact Table: ViewingEvent

| Column           | Type    | Key  | Description                                  |
|------------------|---------|------|----------------------------------------------|
| ViewingEventKey  | BIGINT  | PK   | Surrogate key for each viewing event         |
| UserKey          | INT     | FK   | Links to DimUser                             |
| ContentKey       | INT     | FK   | Links to DimContent                          |
| DateKey          | INT     | FK   | Links to DimDate                             |
| TimeKey          | INT     | FK   | Links to DimTime                             |
| DeviceKey        | INT     | FK   | Links to DimDevice                           |
| PlanKey          | INT     | FK   | Links to DimSubscriptionPlan                 |
| GeographyKey     | INT     | FK   | Links to DimGeography                        |
| DurationWatched  | INT     |      | Total seconds watched                        |
| CompletedFlag    | BIT     |      | 1 if watched to completion, else 0           |
| PauseCount       | INT     |      | Number of pauses                             |
| RewindCount      | INT     |      | Number of rewinds                            |
| LoadDate         | DATETIME|      | Timestamp when the record was loaded         |

## Dimension Tables

### DimUser

| Column      | Type      | Key  | Description                                        |
|-------------|-----------|------|----------------------------------------------------|
| UserKey     | INT       | PK   | Surrogate key for each user                        |
| UserID      | VARCHAR   |      | Business key from user system                      |
| Gender      | CHAR(1)   |      | M or F                                             |
| BirthYear   | SMALLINT  |      | Year of birth                                      |
| SignupDate  | DATE      |      | When user signed up                                |
| Region      | VARCHAR   |      | User’s geographic region                           |
| PlanKey     | INT       | FK   | Current subscription plan                          |
| IsCurrent   | BIT       |      | Flag for current SCD Type 2 record                 |

### DimContent

| Column         | Type     | Key  | Description                                  |
|----------------|----------|------|----------------------------------------------|
| ContentKey     | INT      | PK   | Surrogate key for each title                 |
| ContentID      | VARCHAR  |      | Business key from content system             |
| Title          | VARCHAR  |      | Movie or show name                           |
| ContentType    | VARCHAR  |      | Movie, Series, Documentary                    |
| ReleaseYear    | SMALLINT |      | Year released                                  |
| Language       | VARCHAR  |      | Primary audio language                        |
| MaturityRating | VARCHAR  |      | PG-13, R, etc.                                |
| RuntimeMinutes | INT      |      | Duration in minutes                           |

### BridgeContentGenre

| Column     | Type | Key    | Description              |
|------------|------|--------|--------------------------|
| ContentKey | INT  | PK,FK  | Links to DimContent      |
| GenreKey   | INT  | PK,FK  | Links to DimGenre        |

### DimGenre

| Column    | Type    | Key  | Description             |
|-----------|---------|------|-------------------------|
| GenreKey  | INT     | PK   | Surrogate key for genre |
| GenreName | VARCHAR |      | Drama, Comedy, Sci-Fi   |

### DimDate

| Column      | Type     | Key  | Description                 |
|-------------|----------|------|-----------------------------|
| DateKey     | INT      | PK   | Surrogate key               |
| FullDate    | DATE     |      | Calendar date               |
| DayOfWeek   | VARCHAR  |      | Monday–Sunday               |
| Month       | VARCHAR  |      | January–December            |
| Quarter     | TINYINT  |      | 1–4                         |
| Year        | SMALLINT |      | Four-digit year             |
| IsHoliday   | BIT      |      | Flag for public holiday     |

### DimTime

| Column       | Type     | Key  | Description                         |
|--------------|----------|------|-------------------------------------|
| TimeKey      | INT      | PK   | Surrogate key                       |
| HourOfDay    | TINYINT  |      | 0–23                                |
| MinuteOfHour | TINYINT  |      | 0–59                                |
| TimeSlot     | VARCHAR  |      | Morning/Afternoon/Evening/Night     |

### DimDevice

| Column         | Type     | Key  | Description                         |
|----------------|----------|------|-------------------------------------|
| DeviceKey      | INT      | PK   | Surrogate key                       |
| DeviceType     | VARCHAR  |      | TV, Mobile, Tablet, PC             |
| OperatingSystem| VARCHAR  |      | OS name and version                |
| AppVersion     | VARCHAR  |      | Netflix app version                |

### DimSubscriptionPlan

| Column      | Type     | Key  | Description                           |
|-------------|----------|------|---------------------------------------|
| PlanKey     | INT      | PK   | Surrogate key                         |
| PlanName    | VARCHAR  |      | Basic, Standard, Premium              |
| MonthlyFee  | DECIMAL  |      | Price per month                       |
| MaxScreens  | TINYINT  |      | Concurrent streams allowed            |
| HDSupport   | BIT      |      | HD streaming enabled                  |

### DimGeography

| Column       | Type     | Key  | Description                               |
|--------------|----------|------|-------------------------------------------|
| GeographyKey | INT      | PK   | Surrogate key                             |
| Country      | VARCHAR  |      | Country name                              |
| Region       | VARCHAR  |      | State or province                         |
| TimeZone     | VARCHAR  |      | Time zone identifier                      |

## Using the Model for Analysis

This dimensional setup enables fast, flexible queries by joining the fact table to dimensions.  

- Analyze viewing behavior by user segments: gender, age group, or region.  
- Track content popularity over time: watch counts, completion rates, average watch time.  
- Drill into genre trends via the content–genre bridge.  
- Observe device usage patterns: compare TV vs mobile engagement by market.  
- Measure plan performance: churn risk by plan tier, upgrade likelihood.  
- Seasonal analysis: assess holiday spikes or weekday vs weekend viewing habits.  

### Example Analytical Queries

1. Monthly active users and average watch time by age group.  
2. Top 10 most binge-watched series in the last quarter.  
3. Average pause count and rewind behavior by device type.  
4. Revenue impact: correlate subscription fee tiers to total watch hours.  
5. Geography-based heatmap: visualize per-capita viewing minutes.  
