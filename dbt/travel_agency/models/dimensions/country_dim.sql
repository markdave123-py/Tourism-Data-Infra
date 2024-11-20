SELECT
    ROW_NUMBER() OVER () AS country_id,
    country_name,
    official_name,
    native_name,
    capital,
    region,
    sub_region,
    languages,
    population
FROM {{ ref('stg_country_data') }}
