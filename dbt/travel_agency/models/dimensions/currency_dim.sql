SELECT
    ROW_NUMBER() OVER () AS currency_id,
    country_name,
    currency_code,
    currency_name,
    currency_symbol
FROM {{ ref('stg_country_data') }}
