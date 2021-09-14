# import sqlite3

create_job = """CREATE TABLE "job" (
    "job_id" INTEGER,
    "site" TEXT,
    "site_counter" INTEGER,
    "collected_at" TEXT,
    "parameters" TEXT,
    "records" INTEGER,
    "out_file" TEXT,
    PRIMARY KEY("job_id" AUTOINCREMENT)
);"""

create_antallaktika = """CREATE TABLE "antallaktikaonline" (
    "job_id" INTEGER,
    "article_no" TEXT,
    "price_after_discount" REAL,
    "retail_price" REAL,
    "availability" TEXT,
    "img" TEXT,
    "recycler" TEXT,
    "kit" INTEGER,
    FOREIGN KEY("job_id") REFERENCES "job"("job_id")
);"""


update_job = """INSERT INTO
    "job" (
        "site",
        "site_counter",
        "collected_at",
        "parameters",
        "records",
        "out_file"
    )
VALUES
    (
        :site,
        :site_counter,
        :collected_at,
        :parameters,
        :records,
        :out_file
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

create_rellas = """CREATE TABLE "rellasamortiser" (
    "job_id" INTEGER,
    "title" TEXT,
    "article_no" TEXT,
    "retail_price" REAL,
    "model" TEXT,
    "year" TEXT,
    "manufacturer" TEXT,
    FOREIGN KEY("job_id") REFERENCES "job"("job_id")
);"""

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
