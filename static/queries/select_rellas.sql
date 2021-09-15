SELECT
    "title",
    "sku",
    "retail_price",
    "model",
    "year",
    "manufacturer"
FROM
    rellasamortiser
WHERE
    job_id = :job_id