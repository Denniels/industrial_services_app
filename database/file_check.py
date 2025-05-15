import psycopg2

def check_db():
    with open('db_check_results.txt', 'w') as f:
        try:
            # Test postgres connection
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='admin',
                host='localhost',
                port='5432'
            )
            f.write("Connected to postgres database\n")
            
            with conn.cursor() as cur:
                cur.execute('SELECT version()')
                version = cur.fetchone()
                f.write(f"PostgreSQL version: {version[0]}\n")
            
            conn.close()
            
            # Test integral_service_db connection
            conn = psycopg2.connect(
                dbname='integral_service_db',
                user='postgres',
                password='admin',
                host='localhost',
                port='5432'
            )
            f.write("\nConnected to integral_service_db\n")
            
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = cur.fetchall()
                f.write("\nTables found:\n")
                for table in tables:
                    f.write(f"  - {table[0]}\n")
            
            f.write("\nVerification completed successfully")
            return True
        except Exception as e:
            f.write(f"\nError: {str(e)}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == '__main__':
    check_db()
