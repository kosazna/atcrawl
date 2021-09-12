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
        "job_id",
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
        :job_id,
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
        "job_id",
        "title",
        "article_no",
        "retail_price",
        "model",
        "year",
        "manufacturer"
    )
VALUES
    (
        :job_id,
        :title,
        :article_no,
        :retail_price,
        :model,
        :year,
        :manufacturer
    )"""
