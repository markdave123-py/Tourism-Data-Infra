SELECT
    ROW_NUMBER() OVER () AS fact_id,
    c.country_id,
    cu.currency_id,
    g.geography_id,
    m.membership_id,
    c.population,
    g.area,
    CURRENT_DATE AS date_loaded
FROM {{ ref('country_dim') }} c
LEFT JOIN {{ ref('currency_dim') }} cu ON c.country_name = cu.country_name
LEFT JOIN {{ ref('geography_dim') }} g ON c.country_name = g.country_name
LEFT JOIN {{ ref('membership_dim') }} m ON c.country_name = m.country_name
