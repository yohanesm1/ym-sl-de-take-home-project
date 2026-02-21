CREATE SCHEMA IF NOT EXISTS analytics;

-- ----------------------------------------------------------------------------
-- 1. COLLISION SUMMARY - Basic aggregations for 2024
-- ----------------------------------------------------------------------------
-- ----------------------------------------------------------------------------
-- 1. COLLISION SUMMARY - Basic aggregations for 2024
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.collision_summary;

CREATE TABLE analytics.collision_summary AS
SELECT
    COUNT(*) AS total_collisions,
    SUM(CASE WHEN CAST(number_of_persons_injured AS INTEGER) > 0 THEN 1 ELSE 0 END) AS injury_incidents,
    SUM(CASE WHEN CAST(number_of_persons_killed AS INTEGER) > 0 THEN 1 ELSE 0 END) AS fatal_incidents,
    SUM(CAST(number_of_persons_injured AS INTEGER)) AS total_persons_injured,
    SUM(CAST(number_of_persons_killed AS INTEGER)) AS total_persons_killed,
    SUM(CAST(number_of_pedestrians_injured AS INTEGER)) AS pedestrians_injured,
    SUM(CAST(number_of_pedestrians_killed AS INTEGER)) AS pedestrians_killed,
    SUM(CAST(number_of_cyclist_injured AS INTEGER)) AS cyclists_injured,
    SUM(CAST(number_of_cyclist_killed AS INTEGER)) AS cyclists_killed,
    SUM(CAST(number_of_motorist_injured AS INTEGER)) AS motorists_injured,
    SUM(CAST(number_of_motorist_killed AS INTEGER)) AS motorists_killed
FROM raw.collision_crashes;

-- ----------------------------------------------------------------------------
-- 2. FACT CRASHES - one row per crash (typed + derived fields)
-- ----------------------------------------------------------------------------
-- ----------------------------------------------------------------------------
-- 2. FACT CRASHES - One row per crash (typed + derived fields)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.fact_crashes;

CREATE TABLE analytics.fact_crashes AS
SELECT
    CAST(collision_id AS BIGINT) AS collision_id,
    CAST(crash_date AS DATE) AS crash_date,
    CAST(crash_time AS TIME) AS crash_time,

    -- geography
    borough,
    on_street_name,
    cross_street_name,
    off_street_name,
    zip_code,

    -- coordinates
    CAST(latitude AS DOUBLE PRECISION) AS latitude,
    CAST(longitude AS DOUBLE PRECISION) AS longitude,

    -- counts
    CAST(number_of_persons_injured AS INTEGER) AS persons_injured,
    CAST(number_of_persons_killed AS INTEGER) AS persons_killed,
    CAST(number_of_pedestrians_injured AS INTEGER) AS pedestrians_injured,
    CAST(number_of_pedestrians_killed AS INTEGER) AS pedestrians_killed,
    CAST(number_of_cyclist_injured AS INTEGER) AS cyclists_injured,
    CAST(number_of_cyclist_killed AS INTEGER) AS cyclists_killed,
    CAST(number_of_motorist_injured AS INTEGER) AS motorists_injured,
    CAST(number_of_motorist_killed AS INTEGER) AS motorists_killed,

    -- contributing factors
    contributing_factor_vehicle_1,
    contributing_factor_vehicle_2,
    contributing_factor_vehicle_3,
    contributing_factor_vehicle_4,
    contributing_factor_vehicle_5,

    -- derived fields
    EXTRACT(HOUR FROM CAST(crash_time AS TIME)) AS crash_hour,
    EXTRACT(DOW FROM CAST(crash_date AS DATE)) AS crash_dow,
    EXTRACT(MONTH FROM CAST(crash_date AS DATE)) AS crash_month,

    CASE WHEN CAST(number_of_persons_injured AS INTEGER) > 0 THEN 1 ELSE 0 END AS is_injury,
    CASE WHEN CAST(number_of_persons_killed AS INTEGER) > 0 THEN 1 ELSE 0 END AS is_fatal

FROM raw.collision_crashes;