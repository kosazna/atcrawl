CREATE TABLE "job" (
    "job_id" INTEGER,
    "site" TEXT,
    "site_counter" INTEGER,
    "collected_at" TEXT,
    "parameters" TEXT,
    "records" INTEGER,
    "out_file" TEXT,
    PRIMARY KEY("job_id" AUTOINCREMENT)
);