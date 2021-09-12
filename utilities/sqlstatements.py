# import sqlite3

update_job = """INSERT INTO
    "job" (
        "site",
        "site_counter",
        "run_at",
        "parameters",
        "records"
    )
VALUES
    (
        :site,
        :site_counter,
        :run_at,
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

update_jobid = """UPDATE
    :table
SET
    job_id = :job_id,
WHERE
    job_id IS NULL"""
