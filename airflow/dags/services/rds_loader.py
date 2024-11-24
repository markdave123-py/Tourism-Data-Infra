from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging


def rds_loader(data_batch):
    try:
        # Initialize database connection
        hook = PostgresHook(postgres_conn_id="rds_postgres")
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Insert query
        insert_query = """
        INSERT INTO country_data (
            country_name, official_name, native_name, independence, un_member,
            start_of_week, currency_code, currency_name, currency_symbol,
            country_code, capital, region, sub_region, languages, area,
            population, continents
        ) VALUES (
            %(country_name)s, %(official_name)s, %(native_name)s, %(independence)s, %(un_member)s,
            %(start_of_week)s, %(currency_code)s, %(currency_name)s, %(currency_symbol)s,
            %(country_code)s, %(capital)s, %(region)s, %(sub_region)s, %(languages)s, %(area)s,
            %(population)s, %(continents)s
        ) ON CONFLICT (country_name, date_loaded) DO NOTHING;
        """

        # Execute batch insert
        logging.info(
            f"Attempting to insert {len(data_batch)} rows into the database.")
        cursor.executemany(insert_query, data_batch)
        conn.commit()
        logging.info(
            f"Successfully loaded {len(data_batch)} rows into the database.")
    except Exception as e:
        logging.error(f"Error loading data to RDS: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
