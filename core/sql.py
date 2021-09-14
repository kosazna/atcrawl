# import sqlite3
from pathlib import Path
from sqlite3 import connect, Error
from contextlib import closing
from subprocess import Popen
from atcrawl.utilities.data import ItemCollection
from atcrawl.utilities.sqlstatements import *
from datetime import datetime


class AtcrawlSQL:
    def __init__(self, db) -> None:
        self.db = db
        self._check_db_exists()

    def _check_db_exists(self):
        if Path(self.db).exists():
            pass
        else:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(create_job)
                    cur.execute(create_antallaktika)
                    cur.execute(create_rellas)

    def update_job(self, site, site_counter, collected_at, parameters, records):
        params = {'site': site,
                  'site_counter': site_counter,
                  'collected_at': collected_at,
                  'parameters': parameters,
                  'records': records}
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(update_job, params)
                    con.commit()

        except Error as e:
            print(str(e) + " from " + self.db)

    def update_antallaktika(self, data):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.executemany(update_antallaktika, data)
                    con.commit()

        except Error as e:
            print(str(e) + " from " + self.db)

    def update_jobid(self, table, job_id):
        tables = {'antallaktikaonline': update_jobid_antallaktika,
                  'rellasamortiser': update_jobid_rellas}
        params = {'job_id': job_id}
        query = tables[table]
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(query, params)
                    con.commit()

        except Error as e:
            print(str(e) + " from " + self.db)

    def update_records(self, table, data):
        tables = {'antallaktikaonline': update_antallaktika,
                  'rellasamortiser': update_rellas}
        query = tables[table]
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.executemany(query, data)
                    con.commit()

        except Error as e:
            print(str(e) + " from " + self.db)

    def update_rellas(self, data):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.executemany(update_rellas, data)
                    con.commit()

        except Error as e:
            print(str(e) + " from " + self.db)

    def get_last_jobid(self):
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(get_last_jobid)

                    val = cur.fetchone()
                    return 1 if val is None else val[0]
        except Error as e:
            print(str(e) + " from " + self.db)

    def get_site_counter(self, site):
        params = {'site': site}
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(get_site_counter, params)

                    return cur.fetchone()[0]
        except Error as e:
            print(str(e) + " from " + self.db)

    def get_records_from_jobid(self, table, job_id):
        tables = {'antallaktikaonline': select_antallaktika,
                  'rellasamortiser': select_rellas}
        params = {'job_id': job_id}
        query = tables[table]
        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(query, params)

                    cols = [description[0] for description in cur.description]
                    data = cur.fetchall()

                    return cols, data
        except Error as e:
            print(str(e) + " from " + self.db)

    def backup(self, process: str, parameters: dict, collection: ItemCollection, out_file:str):
        table = process.split('.')[0]
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            with closing(connect(self.db)) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(get_site_counter, {'site': process})
                    site_counter = cur.fetchone()[0] + 1

                    params = {'site': process,
                              'site_counter': site_counter,
                              'collected_at': date,
                              'parameters': parameters,
                              'records': collection.nitems,
                              'out_file': out_file}
                    cur.execute(update_job, params)

                    cur.execute(get_last_jobid)
                    val = cur.fetchone()
                    last_job = 1 if val is None else val[0]

                    tables = {'antallaktikaonline': update_antallaktika,
                              'rellasamortiser': update_rellas}
                    query = tables[table]
                    cur.executemany(query, collection.get_data('tuple'))
                    con.commit()

                    tables = {'antallaktikaonline': update_jobid_antallaktika,
                              'rellasamortiser': update_jobid_rellas}
                    query = tables[table]
                    cur.execute(query, {'job_id': last_job})

                    con.commit()
        except Error as e:
            print(str(e) + " from " + self.db)


if __name__ == '__main__':
    # Popen(["C:/Program Files/DB Browser for SQLite/DB Browser for SQLite.exe", "D:/ktima.db"])
    asql = AtcrawlSQL("C:/Users/aznavouridis.k/.atcrawl/atcrawl.db")

    print(asql.get_records_from_jobid('antallaktikaonline', 5))
