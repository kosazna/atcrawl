# import sqlite3
from sqlite3 import connect, Error
from contextlib import closing
from subprocess import Popen
from atcrawl.utilities.sqlstatements import *


class AtcrawlSQL:
    def __init__(self, db) -> None:
        self.db = db

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

                    return cur.fetchone()[0]
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

                    return cur.fetchall()
        except Error as e:
            print(str(e) + " from " + self.db)

    # def get_otas(self, company_name='NAMA'):
    #     params = {'meleti': self.meleti,
    #               'company_name': company_name}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(ota_query, params)

    #                 return tuple([row[0] for row in cur.fetchall()])
    #     except Error as e:
    #         print(str(e) + " from " + self.db)
    #         return []

    # def get_shapes(self, ktima_type):
    #     params = {'meleti': self.meleti,
    #               'ktima_type': ktima_type}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(shape_query, params)

    #                 return tuple([row[0] for row in cur.fetchall()])
    #     except Error as e:
    #         print(str(e) + " from " + self.db)
    #         return []

    # def get_locality(self):
    #     params = {'meleti': self.meleti}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(locality_query, params)

    #                 return tuple(cur.fetchall())
    #     except Error as e:
    #         print(str(e) + " from " + self.db)
    #         return []

    # def get_fbound_docs(self):
    #     params = {'meleti': self.meleti}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(fbound_query, params)

    #                 return tuple(cur.fetchall())
    #     except Error as e:
    #         print(str(e) + " from " + self.db)
    #         return []

    # def get_overlaps(self):
    #     params = {'meleti': self.meleti,
    #               'mode': self.mode, }
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(overlaps_query, params)

    #                 return cur.fetchone()
    #     except Error as e:
    #         print(str(e) + " from " + self.db)

    # def update_overlaps(self, check_date, decimals, astenot, asttom, pst):
    #     params = {'meleti': self.meleti,
    #               'mode': self.mode,
    #               'check_date': check_date,
    #               'decimals': decimals,
    #               'astenot': astenot,
    #               'asttom': asttom,
    #               'pst': pst}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(update_overlaps_query, params)
    #                 con.commit()

    #     except Error as e:
    #         print(str(e) + " from " + self.db)

    # def get_geometry(self, shape):
    #     params = {'meleti': self.meleti,
    #               'mode': self.mode,
    #               'shape': shape}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(geometry_query, params)

    #                 return cur.fetchone()
    #     except Error as e:
    #         print(str(e) + " from " + self.db)

    # def update_geometry(self, shape, check_date, has_probs, ota):
    #     params = {'meleti': self.meleti,
    #               'mode': self.mode,
    #               'shape': shape,
    #               'check_date': check_date,
    #               'has_probs': has_probs,
    #               'ota': ota}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(update_geometry_query, params)
    #                 con.commit()

    #     except Error as e:
    #         print(str(e) + " from " + self.db)

    # def update_logs(self, timestamp, user, action, comments):
    #     params = {'timestamp': timestamp,
    #               'user': user,
    #               'meleti': self.meleti,
    #               'action': action,
    #               'comments': comments}
    #     try:
    #         with closing(connect(self.db)) as con:
    #             with closing(con.cursor()) as cur:
    #                 cur.execute(update_logs, params)
    #                 con.commit()

    #     except Error as e:
    #         print(str(e) + " from " + self.db)


if __name__ == '__main__':
    # Popen(["C:/Program Files/DB Browser for SQLite/DB Browser for SQLite.exe", "D:/ktima.db"])
    asql = AtcrawlSQL("C:/Users/aznavouridis.k/.atcrawl/atcrawl.db")

    print(asql.get_records_from_jobid('antallaktikaonline', 5))