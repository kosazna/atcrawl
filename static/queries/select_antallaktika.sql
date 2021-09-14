SELECT
    "article_no",
    "price_after_discount",
    "retail_price",
    "availability",
    "img",
    "recycler",
    "kit"
FROM
    antallaktikaonline
WHERE
    job_id = :job_id