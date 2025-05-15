import psycopg2

def main():
    try:
        # Test postgres connection
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        print("Connected to postgres database")
        
        with conn.cursor() as cur:
            cur.execute('SELECT version()')
            version = cur.fetchone()
            print(f"PostgreSQL version: {version[0]}")
        
        conn.close()
        
        # Test integral_service_db connection
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        print("\nConnected to integral_service_db")
        
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()
            print("\nTables found:")
            for table in tables:
                print(f"  - {table[0]}")
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    main()
