import psycopg2

class ScannerDb:

    def count_rows_all_tables(self, db_name='FrotasCasteloBranco', user='FrotasCasteloBranco', password='es74079', host='localhost', port='5432'):
        results = []
        try:
            # Establish a connection to the database
            conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)

            with conn:
                with conn.cursor() as cur:
                    # Get all table names
                    cur.execute("""
                        SELECT table_schema, table_name
                        FROM information_schema.tables
                        WHERE table_type = 'BASE TABLE'
                        AND table_schema NOT IN ('pg_catalog', 'information_schema');
                    """)
                    tables = cur.fetchall()

                    for table in tables:
                        table_full_name = f"{table[0]}.{table[1]}"
                        # Count rows in the current table
                        cur.execute(f"""
                            SELECT COUNT(*)
                            FROM {table_full_name};
                        """)
                        count = cur.fetchone()[0]
                        results.append((table_full_name, count))

        except psycopg2.Error as e:
            print(f"An error occurred: {e}")

        return results

    def search_table_for_value(self, table_name, search_value, db_name='FrotasCasteloBranco', user='FrotasCasteloBranco', password='es74079', host='localhost', port='5432'):
        try:
            # Establish a connection to the database
            conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)

            with conn:
                with conn.cursor() as cur:
                    # Get all column names in the table
                    cur.execute(f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{table_name.split('.')[1]}'
                    """)
                    columns = cur.fetchall()

                    for column in columns:
                        cur.execute(f"""SELECT EXISTS (SELECT 1 FROM {table_name} WHERE upper(CAST({column[0]} AS TEXT)) LIKE upper('%{search_value}%'))""")
                        resp = (cur.fetchone()[0])
                        if resp:
                            return (f"""SELECT * FROM {table_name} WHERE upper(CAST({column[0]} AS TEXT)) LIKE upper('%{search_value}%')""")

        except psycopg2.Error as e:
            print(f"An error occurred: {e}")

