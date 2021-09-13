CREATE TABLE "antallaktikaonline" (
    "job_id" INTEGER,
    "article_no" TEXT,
    "price_after_discount" REAL,
    "retail_price" REAL,
    "availability" TEXT,
    "img" TEXT,
    "recycler" TEXT,
    "kit" INTEGER,
    FOREIGN KEY("job_id") REFERENCES "job"("job_id")
);