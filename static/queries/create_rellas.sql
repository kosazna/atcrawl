CREATE TABLE "rellasamortiser" (
    "job_id" INTEGER,
    "title" TEXT,
    "sku" TEXT,
    "retail_price" REAL,
    "model" TEXT,
    "year" TEXT,
    "manufacturer" TEXT,
    FOREIGN KEY("job_id") REFERENCES "job"("job_id")
);