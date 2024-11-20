SELECT
    ROW_NUMBER() OVER () AS geography_id,
    country_name,
    area,
    continents
FROM {{ ref('stg_country_data') }}
