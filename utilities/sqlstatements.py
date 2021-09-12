# import sqlite3

update_job = """INSERT INTO
    "job" (
        "site",
        "site_counter",
        "collected_at",
        "parameters",
        "records"
    )
VALUES
    (
        :site,
        :site_counter,
        :collected_at,
        :parameters,
        :records
    )"""

update_antallaktika = """INSERT INTO
    "antallaktikaonline" (
        "article_no",
        "price_after_discount",
        "retail_price",
        "availability",
        "img",
        "recycler",
        "kit"
    )
VALUES
    (
        :article_no,
        :price_after_discount,
        :retail_price,
        :availability,
        :img,
        :recycler,
        :kit
    )"""

update_rellas = """INSERT INTO
    "rellasamortiser" (
        "title",
        "article_no",
        "retail_price",
        "model",
        "year",
        "manufacturer"
    )
VALUES
    (
        :title,
        :article_no,
        :retail_price,
        :model,
        :year,
        :manufacturer
    )"""

update_jobid_antallaktika = """UPDATE
    antallaktikaonline
SET
    job_id = :job_id
WHERE
    job_id IS NULL"""

update_jobid_rellas = """UPDATE
    rellasamortiser
SET
    job_id = :job_id
WHERE
    job_id IS NULL"""

get_last_jobid = """SELECT job_id
FROM job
ORDER BY job_id DESC
LIMIT 1"""

get_site_counter = """SELECT
    COUNT(site_counter)
FROM
    job
WHERE
    site = :site"""

select_antallaktika = """SELECT
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
    job_id = :job_id"""

select_rellas = """SELECT
    "title",
    "article_no",
    "retail_price",
    "model",
    "year",
    "manufacturer"
FROM
    rellasamortiser
WHERE
    job_id = :job_id"""
