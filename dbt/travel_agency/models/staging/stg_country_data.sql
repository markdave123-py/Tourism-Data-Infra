
SELECT
    country_name AS country_name,
    official_name AS official_name,
    native_name AS native_name,
    COALESCE(independence, FALSE) AS independence,
    COALESCE(un_member, FALSE) AS un_member,
    start_of_week AS start_of_week,
    currency_code AS currency_code,
    currency_name AS currency_name,
    currency_symbol AS currency_symbol,
    country_code AS country_code,
    capital AS capital,
    region AS region,
    COALESCE(sub_region, '') AS sub_region,
    languages AS languages,
    CAST(area AS FLOAT) AS area,
    CAST(population AS BIGINT) AS population,
    continents AS continents
FROM {{ source('public', 'country_data') }}