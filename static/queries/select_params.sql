SELECT
    collected_at,
    records,
    parameters
FROM
    job
WHERE
    job_id = :job_id