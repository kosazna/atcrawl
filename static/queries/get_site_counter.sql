SELECT
    COUNT(site_counter)
FROM
    job
WHERE
    site = :site