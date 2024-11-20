SELECT
    ROW_NUMBER() OVER () AS membership_id,
    country_name,
    independence,
    un_member,
    start_of_week
FROM {{ ref('stg_country_data') }}
