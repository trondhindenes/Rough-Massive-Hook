import rethinkdb as r

class RethinkDbHelper(object):
    @staticmethod
    def ensure_database_and_table(rethinkdb_host, rethinkdb_port, rethinkdb_db, rethinkdb_table):
        r.connect(rethinkdb_host, rethinkdb_port).repl()
        databases = r.db_list().run()
        this_db = [x for x in databases if x == rethinkdb_db]
        if this_db.__len__() == 0:
            r.db_create(rethinkdb_db).run()
        tables = r.db(rethinkdb_db).table_list().run()
        this_table = [x for x in tables if x == rethinkdb_table]
        if this_table.__len__() == 0:
            r.db(rethinkdb_db).table_create(rethinkdb_table).run()

    @staticmethod
    def get_item(self):
        pass
